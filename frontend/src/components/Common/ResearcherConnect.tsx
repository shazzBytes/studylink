import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Globe, Linkedin, Mail } from "lucide-react"

interface ResearcherConnectProps {
  email: string
  linkedin?: string
  website?: string
}

export function ResearcherConnect({ email, linkedin, website }: ResearcherConnectProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Connect</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" size="sm" asChild>
            <a href={`mailto:${email}`}>
              <Mail className="mr-2 h-4 w-4" />
              Email
            </a>
          </Button>
          {linkedin && (
            <Button variant="outline" size="sm" asChild>
              <a href={linkedin} target="_blank" rel="noopener noreferrer">
                <Linkedin className="mr-2 h-4 w-4" />
                LinkedIn
              </a>
            </Button>
          )}
          {website && (
            <Button variant="outline" size="sm" asChild>
              <a href={website} target="_blank" rel="noopener noreferrer">
                <Globe className="mr-2 h-4 w-4" />
                Website
              </a>
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
