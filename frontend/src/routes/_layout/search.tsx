import { createFileRoute } from "@tanstack/react-router"
import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ResearcherCard } from "@/components/Common/ResearcherCard"
import { Search, X, Filter } from "lucide-react"

export const Route = createFileRoute("/_layout/search")({
  component: SearchPage,
})

function SearchPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedInterests, setSelectedInterests] = useState<string[]>([])
  const [selectedLocations, setSelectedLocations] = useState<string[]>([])

  // Mock data - replace with actual API call
  const availableInterests = [
    "Deep Learning",
    "Computer Vision",
    "Natural Language Processing",
    "Machine Learning",
    "Robotics",
    "Neural Networks",
    "AI Ethics",
  ]

  const availableLocations = [
    "Cambridge, MA",
    "Stanford, CA",
    "New York, NY",
    "London, UK",
    "Toronto, ON",
  ]

  const researchers = [
    {
      id: "1",
      name: "Dr. Alice Brown",
      role: "Associate Professor",
      affiliation: "Massachusetts Institute of Technology",
      location: "Cambridge, MA",
      avatarUrl: "https://api.dicebear.com/7.x/avataaars/svg?seed=Alice",
      researchInterests: ["Deep Learning", "Computer Vision", "Neural Networks"],
      stats: {
        publications: 47,
        citations: 3245,
      },
    },
    {
      id: "2",
      name: "Dr. John Smith",
      role: "Professor",
      affiliation: "Stanford University",
      location: "Stanford, CA",
      avatarUrl: "https://api.dicebear.com/7.x/avataaars/svg?seed=John",
      researchInterests: ["Natural Language Processing", "Machine Learning", "AI Ethics"],
      stats: {
        publications: 89,
        citations: 5432,
      },
    },
    {
      id: "3",
      name: "Dr. Sarah Johnson",
      role: "Senior Researcher",
      affiliation: "Google DeepMind",
      location: "London, UK",
      avatarUrl: "https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah",
      researchInterests: ["Robotics", "Deep Learning", "Computer Vision"],
      stats: {
        publications: 62,
        citations: 4123,
      },
    },
    {
      id: "4",
      name: "Dr. Michael Chen",
      role: "Assistant Professor",
      affiliation: "University of Toronto",
      location: "Toronto, ON",
      avatarUrl: "https://api.dicebear.com/7.x/avataaars/svg?seed=Michael",
      researchInterests: ["Machine Learning", "Neural Networks", "AI Ethics"],
      stats: {
        publications: 34,
        citations: 1876,
      },
    },
  ]

  const toggleInterest = (interest: string) => {
    setSelectedInterests((prev) =>
      prev.includes(interest)
        ? prev.filter((i) => i !== interest)
        : [...prev, interest]
    )
  }

  const toggleLocation = (location: string) => {
    setSelectedLocations((prev) =>
      prev.includes(location)
        ? prev.filter((l) => l !== location)
        : [...prev, location]
    )
  }

  const clearFilters = () => {
    setSelectedInterests([])
    setSelectedLocations([])
    setSearchQuery("")
  }

  // Filter researchers based on search query and filters
  const filteredResearchers = researchers.filter((researcher) => {
    const matchesSearch =
      searchQuery === "" ||
      researcher.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      researcher.affiliation.toLowerCase().includes(searchQuery.toLowerCase()) ||
      researcher.researchInterests.some((interest) =>
        interest.toLowerCase().includes(searchQuery.toLowerCase())
      )

    const matchesInterests =
      selectedInterests.length === 0 ||
      selectedInterests.some((interest) =>
        researcher.researchInterests.includes(interest)
      )

    const matchesLocation =
      selectedLocations.length === 0 ||
      selectedLocations.includes(researcher.location)

    return matchesSearch && matchesInterests && matchesLocation
  })

  const hasActiveFilters =
    selectedInterests.length > 0 || selectedLocations.length > 0 || searchQuery !== ""

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
              </div>

              {/* Location Filter */}
              <div className="space-y-2">
                <h4 className="text-sm font-semibold">Location</h4>
                <div className="flex flex-wrap gap-1.5">
                  {availableLocations.map((location) => (
                    <Badge
                      key={location}
                      variant={
                        selectedLocations.includes(location) ? "default" : "outline"
                      }
                      className="cursor-pointer text-xs"
                      onClick={() => toggleLocation(location)}
                    >
                      {location}
                      {selectedLocations.includes(location) && (
                        <X className="ml-1 h-3 w-3" />
                      )}
                    </Badge>
                  ))}
                </div>
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
