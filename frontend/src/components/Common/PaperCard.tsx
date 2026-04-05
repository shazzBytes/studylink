import { Link } from "@tanstack/react-router"
import { AspectRatio } from "@/components/ui/aspect-ratio"
import { cn } from "@/lib/utils"
import { BadgeCheck, Eye } from "lucide-react"

interface PaperCardProps {
  title: string
  author: string
  publishedDate: string
  summary: string
  coverImageUrl: string
  impressions?: number
  isVerified?: boolean
  compact?: boolean
  className?: string
  paperId?: string
}

export function PaperCard({
  title,
  author,
  publishedDate,
  summary,
  coverImageUrl,
  impressions,
  isVerified = false,
  compact = false,
  className,
  paperId,
}: PaperCardProps) {
  const cardContent = (
    <div className={cn(
      "flex flex-row gap-4 rounded-lg border-2 border-border bg-card p-4 shadow-sm transition-all hover:shadow-md",
      paperId && "hover:-translate-y-0.5 hover:border-primary/50",
      className
    )}>
      <div className="flex-shrink-0">
        <div className={cn("relative", compact ? "w-24" : "w-40")}>
          <AspectRatio ratio={1 / 1.4142}>
            <img 
              src={coverImageUrl} 
              alt={`Cover image for ${title}`} 
              className="h-full w-full rounded-md object-cover" 
            />
          </AspectRatio>
          {isVerified && (
            <div className="absolute top-2 right-2 rounded-full bg-primary p-1.5 shadow-md">
              <BadgeCheck className="h-4 w-4 text-primary-foreground" />
            </div>
          )}
        </div>
      </div>
      
      <div className="flex flex-1 flex-col gap-2">
        <div>
          <h2 className={cn(
            "font-bold tracking-tight",
            compact ? "text-lg" : "text-2xl"
          )}>{title}</h2>
          <p className="text-sm text-muted-foreground">by {author}</p>
          <div className="flex items-center gap-3">
            <p className="text-sm text-muted-foreground">Published: {publishedDate}</p>
            {impressions !== undefined && (
              <div className="flex items-center gap-1 text-sm text-muted-foreground">
                <Eye className="h-3.5 w-3.5" />
                <span>{impressions.toLocaleString()}</span>
              </div>
            )}
          </div>
        </div>
        
        <p className={cn(
          "text-sm leading-relaxed text-muted-foreground",
          compact ? "line-clamp-2" : "line-clamp-3"
        )}>
          {summary}
        </p>
      </div>
    </div>
  )

  if (paperId) {
    return (
      <Link to="/papers/$id" params={{ id: paperId }} className="block">
        {cardContent}
      </Link>
    )
  }

  return cardContent
}
