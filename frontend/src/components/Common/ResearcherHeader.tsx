import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Heart, MapPin, UserPlus, GraduationCap, BadgeCheck } from "lucide-react"

interface ResearcherHeaderProps {
  name: string
  role: string
  affiliation: string
  location: string
  avatarUrl: string
  mentorshipAvailable?: boolean
  onMentorshipClick?: () => void
  stats: {
    publications: number
    citations: number
    hIndex: number
  }
  onFollow?: () => void
  onConnect?: () => void
  verifiedAffiliation?: boolean
}

export function ResearcherHeader({
  name,
  role,
  affiliation,
  location,
  avatarUrl,
  mentorshipAvailable,
  onMentorshipClick,
  stats,
  onFollow,
  onConnect,
  verifiedAffiliation = false,
}: ResearcherHeaderProps) {
  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex flex-col gap-6 md:flex-row md:items-start md:justify-between">
          <div className="flex flex-col gap-4 md:flex-row md:items-start">
            <Avatar className="h-24 w-24">
              <AvatarImage src={avatarUrl} alt={name} />
              <AvatarFallback>{name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
            </Avatar>
            
            <div className="space-y-2">
              <div>
                <div className="flex items-center gap-2 flex-wrap">
                  <h1 className="text-3xl font-bold tracking-tight">{name}</h1>
                  {verifiedAffiliation && (
                    <Badge variant="secondary" className="gap-1">
                      <BadgeCheck className="h-3.5 w-3.5" />
                      Verified affiliation
                    </Badge>
                  )}
                  {mentorshipAvailable && (
                    <>
                      <GraduationCap className="h-6 w-6 text-emerald-600" />
                      <Badge 
                        variant="default" 
                        className="bg-linear-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 cursor-pointer text-white shadow-sm"
                        onClick={onMentorshipClick}
                      >
                        Mentorship Available
                      </Badge>
                    </>
                  )}
                </div>
                <p className="text-lg text-muted-foreground font-semibold">{role}</p>
                <p className="text-sm text-muted-foreground">{affiliation}</p>
                {location ? (
                  <div className="flex items-center gap-1 text-sm text-muted-foreground">
                    <MapPin className="h-3.5 w-3.5" />
                    <span>{location}</span>
                  </div>
                ) : null}
              </div>
              
              <div className="flex gap-4 text-sm">
                <div>
                  <span className="font-semibold">{stats.publications}</span>
                  <span className="text-muted-foreground"> Publications</span>
                </div>
                <div>
                  <span className="font-semibold">{stats.citations}</span>
                  <span className="text-muted-foreground"> Citations</span>
                </div>
                <div>
                  <span className="font-semibold">{stats.hIndex}</span>
                  <span className="text-muted-foreground"> h-index</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={onFollow}>
              <Heart className="mr-2 h-4 w-4" />
              Follow
            </Button>
            <Button size="sm" onClick={onConnect}>
              <UserPlus className="mr-2 h-4 w-4" />
              Connect
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
