import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface ResearcherMentorshipProps {
  available: boolean
  areas: string[]
  note?: string
}

export function ResearcherMentorship({ available, areas, note }: ResearcherMentorshipProps) {
  return (
    <Card id="mentorship-section">
      <CardHeader>
        <CardTitle>Mentorship</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center gap-2">
          <Badge variant={available ? "default" : "secondary"}>
            {available ? "Available" : "Not Available"}
          </Badge>
        </div>
        <div>
          <h4 className="mb-2 font-semibold">Areas of Expertise</h4>
          <div className="flex flex-wrap gap-2">
            {areas.map((area) => (
              <Badge key={area} variant="outline">
                {area}
              </Badge>
            ))}
          </div>
        </div>
        {note && (
          <p className="text-sm text-muted-foreground">{note}</p>
        )}
      </CardContent>
    </Card>
  )
}
