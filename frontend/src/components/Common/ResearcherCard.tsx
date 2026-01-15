import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { MapPin, FileText, Quote } from "lucide-react"
import { Link } from "@tanstack/react-router"

interface ResearcherCardProps {
  id: string
  name: string
  role: string
  affiliation: string
  location: string
  avatarUrl: string
  researchInterests: string[]
  stats: {
    publications: number
    citations: number
  }
}

export function ResearcherCard({
  id,
  name,
  role,
  affiliation,
  location,
  avatarUrl,
  researchInterests,
  stats,
}: ResearcherCardProps) {
  return (
    <Card className="flex flex-col transition-shadow hover:shadow-lg">
      <CardHeader>
        <div className="flex gap-4">
          <Avatar className="h-16 w-16">
            <AvatarImage src={avatarUrl} alt={name} />
            <AvatarFallback>{name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
          </Avatar>
          
          <div className="flex-1 space-y-1">
            <h3 className="font-semibold text-lg leading-tight">{name}</h3>
            <p className="text-sm text-muted-foreground">{role}</p>
            <p className="text-xs text-muted-foreground">{affiliation}</p>
            <div className="flex items-center gap-1 text-xs text-muted-foreground">
              <MapPin className="h-3 w-3" />
              <span>{location}</span>
            </div>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="flex-1 space-y-3">
        <div className="flex flex-wrap gap-1.5">
          {researchInterests.slice(0, 4).map((interest) => (
            <Badge key={interest} variant="secondary" className="text-xs">
              {interest}
            </Badge>
          ))}
          {researchInterests.length > 4 && (
            <Badge variant="outline" className="text-xs">
              +{researchInterests.length - 4} more
            </Badge>
          )}
        </div>
        
        <div className="flex gap-4 text-xs text-muted-foreground">
          <div className="flex items-center gap-1">
            <FileText className="h-3 w-3" />
            <span>{stats.publications} publications</span>
          </div>
          <div className="flex items-center gap-1">
            <Quote className="h-3 w-3" />
            <span>{stats.citations} citations</span>
          </div>
        </div>
      </CardContent>
      
      <CardFooter>
        <Button asChild className="w-full" size="sm">
          <Link to="/researchers/$id" params={{ id }}>
            View Profile
          </Link>
        </Button>
      </CardFooter>
    </Card>
  )
}
