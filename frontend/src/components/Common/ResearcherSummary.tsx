import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface ResearcherSummaryProps {
  bio: string
}

export function ResearcherSummary({ bio }: ResearcherSummaryProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Research Summary</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="leading-relaxed text-muted-foreground">{bio}</p>
      </CardContent>
    </Card>
  )
}
