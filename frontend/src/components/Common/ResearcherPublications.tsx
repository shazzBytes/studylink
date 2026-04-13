import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { PaperCard } from "./PaperCard"

interface Publication {
  id: string
  title: string
  author: string
  publishedDate: string
  summary: string
  coverImageUrl: string
  impressions?: number
  isVerified?: boolean
}

interface ResearcherPublicationsProps {
  publications: Publication[]
}

export function ResearcherPublications({ publications }: ResearcherPublicationsProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Publications</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {publications.map((paper) => (
          <PaperCard
            key={paper.id}
            paperId={paper.id}
            paperRoute="publications"
            title={paper.title}
            author={paper.author}
            publishedDate={paper.publishedDate}
            summary={paper.summary}
            coverImageUrl={paper.coverImageUrl}
            impressions={paper.impressions}
            isVerified={paper.isVerified}
            compact
          />
        ))}
      </CardContent>
    </Card>
  )
}
