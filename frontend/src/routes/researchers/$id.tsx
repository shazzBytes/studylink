import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useQuery } from "@tanstack/react-query"
import { Button } from "@/components/ui/button"
import { ArrowLeft } from "lucide-react"
import { ResearcherHeader } from "@/components/Common/ResearcherHeader"
import { ResearcherSummary } from "@/components/Common/ResearcherSummary"
import { ResearcherInterests } from "@/components/Common/ResearcherInterests"
import { ResearcherPublications } from "@/components/Common/ResearcherPublications"
import { ResearcherMentorship } from "@/components/Common/ResearcherMentorship"
import { ResearcherConnect } from "@/components/Common/ResearcherConnect"
import { ResearchersService } from "@/client"

export const Route = createFileRoute("/researchers/$id")({
  component: ResearcherProfile,
})

function ResearcherProfile() {
  const { id } = Route.useParams()
  const navigate = useNavigate()

  // Fetch researcher data
  const { data: researcher, isLoading: isLoadingResearcher } = useQuery({
    queryKey: ["researcher", id],
    queryFn: () => ResearchersService.getResearcherRoute({ researcherId: id }),
  })

  // Fetch researcher publications
  const { data: publications } = useQuery({
    queryKey: ["researcher-publications", id],
    queryFn: () => ResearchersService.getResearcherPublicationsRoute({ researcherId: id }),
    enabled: !!researcher, // Only fetch publications if researcher exists
  })

  if (isLoadingResearcher) {
    return (
      <div className="container mx-auto space-y-6 px-6 pb-6">
        <div className="text-center py-8">Loading researcher profile...</div>
      </div>
    )
  }

  if (!researcher) {
    return (
      <div className="container mx-auto space-y-6 px-6 pb-6">
        <div className="text-center py-8">Researcher not found</div>
      </div>
    )
  }

  const researcherRecord = researcher as typeof researcher & {
    affiliation_verified?: boolean
    department?: string | null
  }

  const handleMentorshipClick = () => {
    const mentorshipSection = document.getElementById('mentorship-section')
    if (mentorshipSection) {
      mentorshipSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }

  // Transform publications data for the component
  const transformedPublications = publications?.map((pub) => ({
    id: pub.id || "",
    title: pub.title,
    author: researcher.full_name,
    publishedDate: pub.year ? `${pub.year}` : "Unknown",
    summary: pub.description || "No description available",
    coverImageUrl: "https://images.template.net/518306/High-School-Research-Paper-Cover-Page-Template-edit-online.png",
    impressions: (pub as typeof pub & { view_count?: number }).view_count || 0,
    isVerified: researcherRecord.affiliation_verified || false,
  })) || []

  const totalCitations = (publications || []).reduce(
    (sum, publication) =>
      sum +
      ((publication as typeof publication & { citation_count?: number }).citation_count ||
        0),
    0,
  )
  const sortedCitationCounts = (publications || [])
    .map(
      (publication) =>
        (publication as typeof publication & { citation_count?: number }).citation_count || 0,
    )
    .sort((a, b) => b - a)
  const hIndex = sortedCitationCounts.reduce(
    (index, citations, currentIndex) =>
      citations >= currentIndex + 1 ? currentIndex + 1 : index,
    0,
  )

  // Extract domains as research interests
  const researchInterests = publications
    ? Array.from(new Set(publications.flatMap((pub) => pub.domains || [])))
    : []

  return (
    <div className="container mx-auto space-y-6 px-6 pb-6">
      <Button
        variant="ghost"
        size="sm"
        onClick={() => navigate({ to: "/search" })}
        className="mb-4"
      >
        <ArrowLeft className="mr-2 h-4 w-4" />
        Back to Search
      </Button>
      
      <ResearcherHeader
        name={researcher.full_name}
        role={researcher.qualification}
        affiliation={researcher.institute || "Unknown"}
        location={researcherRecord.department || ""}
        avatarUrl={`https://api.dicebear.com/7.x/avataaars/svg?seed=${researcher.full_name}`}
        mentorshipAvailable={false}
        onMentorshipClick={handleMentorshipClick}
        stats={{
          publications: publications?.length || 0,
          citations: totalCitations,
          hIndex,
        }}
        verifiedAffiliation={researcherRecord.affiliation_verified || false}
      />

      {researcher.bio && <ResearcherSummary bio={researcher.bio} />}

      {researchInterests.length > 0 && (
        <ResearcherInterests interests={researchInterests} />
      )}

      {transformedPublications.length > 0 && (
        <ResearcherPublications publications={transformedPublications} />
      )}

      <ResearcherMentorship
        available={false}
        areas={[]}
        note="Mentorship information not available"
      />

      <ResearcherConnect
        email={researcher.email}
        linkedin=""
        website=""
      />
    </div>
  )
}
