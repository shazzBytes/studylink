import { createFileRoute } from "@tanstack/react-router"
import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ResearcherCard } from "@/components/Common/ResearcherCard"
import { Search, X, Filter } from "lucide-react"
import { ResearchersService } from "@/client"

export const Route = createFileRoute("/_layout/search")({
  component: SearchPage,
})

function SearchPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedInterests, setSelectedInterests] = useState<string[]>([])

  // Fetch all researchers
  const { data: researchers = [], isLoading } = useQuery({
    queryKey: ["researchers-search", searchQuery],
    queryFn: () =>
      ResearchersService.searchResearchersRoute({
        fullName: searchQuery || undefined,
        limit: 100,
      }),
  })

  // Fetch publications for all researchers to get research interests
  const { data: allPublications = [] } = useQuery({
    queryKey: ["all-publications"],
    queryFn: async () => {
      const publications = await Promise.all(
        researchers.map((r) =>
          ResearchersService.getResearcherPublicationsRoute({
            researcherId: r.id!,
          }).catch(() => [])
        )
      )
      return publications.flat()
    },
    enabled: researchers.length > 0,
  })

  // Extract unique research interests from all publications
  const availableInterests = Array.from(
    new Set(allPublications.flatMap((pub) => pub.domains || []))
  ).sort()

  const toggleInterest = (interest: string) => {
    setSelectedInterests((prev) =>
      prev.includes(interest)
        ? prev.filter((i) => i !== interest)
        : [...prev, interest]
    )
  }

  const clearFilters = () => {
    setSelectedInterests([])
    setSearchQuery("")
  }

  // Transform researchers data for the ResearcherCard component
  const transformedResearchers = researchers.map((researcher) => {
    const researcherPublications = allPublications.filter(
      (pub) => pub.researcher_id === researcher.id
    )
    const researchInterests = Array.from(
      new Set(researcherPublications.flatMap((pub) => pub.domains || []))
    )

    return {
      id: researcher.id || "",
      name: researcher.full_name,
      role: researcher.qualification,
      affiliation: researcher.institute || "Unknown",
      location: "", // Not available in current API
      avatarUrl: `https://api.dicebear.com/7.x/avataaars/svg?seed=${researcher.full_name}`,
      researchInterests,
      stats: {
        publications: researcherPublications.length,
        citations: 0, // Not available in current API
      },
    }
  })

  // Filter researchers based on selected interests
  const filteredResearchers = transformedResearchers.filter((researcher) => {
    const matchesInterests =
      selectedInterests.length === 0 ||
      selectedInterests.some((interest) =>
        researcher.researchInterests.includes(interest)
      )

    return matchesInterests
  })

  const hasActiveFilters = selectedInterests.length > 0 || searchQuery !== ""

  if (isLoading) {
    return (
      <div className="container mx-auto space-y-6 p-6">
        <div className="text-center py-8">Loading researchers...</div>
      </div>
    )
  }

  return (
    <div className="container mx-auto space-y-6 p-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Search Researchers</h1>
        <p className="text-muted-foreground">
          Find researchers by name, affiliation, or research interests
        </p>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          placeholder="Search by name, affiliation, or interests..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10"
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
        {/* Filters Sidebar */}
        <aside className="space-y-4">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-base flex items-center gap-2">
                  <Filter className="h-4 w-4" />
                  Filters
                </CardTitle>
                {hasActiveFilters && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={clearFilters}
                    className="h-auto p-0 text-xs"
                  >
                    Clear all
                  </Button>
                )}
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Research Interests Filter */}
              <div className="space-y-2">
                <h4 className="text-sm font-semibold">Research Interests</h4>
                {availableInterests.length > 0 ? (
                  <div className="flex flex-wrap gap-1.5">
                    {availableInterests.map((interest) => (
                      <Badge
                        key={interest}
                        variant={
                          selectedInterests.includes(interest) ? "default" : "outline"
                        }
                        className="cursor-pointer text-xs"
                        onClick={() => toggleInterest(interest)}
                      >
                        {interest}
                        {selectedInterests.includes(interest) && (
                          <X className="ml-1 h-3 w-3" />
                        )}
                      </Badge>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-muted-foreground">No interests available</p>
                )}
              </div>
            </CardContent>
          </Card>
        </aside>

        {/* Results */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-sm text-muted-foreground">
              {filteredResearchers.length} researcher
              {filteredResearchers.length !== 1 ? "s" : ""} found
            </p>
          </div>

          {filteredResearchers.length > 0 ? (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3">
              {filteredResearchers.map((researcher) => (
                <ResearcherCard key={researcher.id} {...researcher} />
              ))}
            </div>
          ) : (
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Search className="h-12 w-12 text-muted-foreground/50 mb-4" />
                <h3 className="text-lg font-semibold mb-2">No researchers found</h3>
                <p className="text-sm text-muted-foreground text-center mb-4">
                  Try adjusting your search or filters to find what you're looking for
                </p>
                {hasActiveFilters && (
                  <Button variant="outline" size="sm" onClick={clearFilters}>
                    Clear all filters
                  </Button>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
