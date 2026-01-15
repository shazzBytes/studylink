import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface ResearcherInterestsProps {
  interests: string[]
}

export function ResearcherInterests({ interests }: ResearcherInterestsProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Research Interests</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap gap-2">
          {interests.map((interest) => (
            <Badge key={interest} variant="secondary">
              {interest}
            </Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
