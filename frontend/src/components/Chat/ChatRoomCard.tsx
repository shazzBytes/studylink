import { formatDistanceToNow } from "date-fns"
import { MoreVertical, Users, Archive, LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"
import type { RoomPublic } from "@/types/chat"
import { ConversationType } from "@/types/chat"

interface ChatRoomCardProps {
  room: RoomPublic
  isActive?: boolean
  onClick?: () => void
  onLeave?: () => void
  onArchive?: () => void
}

const getConversationTypeLabel = (type: ConversationType): string => {
  switch (type) {
    case ConversationType.DIRECT:
      return "Direct"
    case ConversationType.GROUP:
      return "Group"
    case ConversationType.MENTORSHIP:
      return "Mentorship"
    case ConversationType.RESEARCH:
      return "Research"
    default:
      return "Unknown"
  }
}

const getInitials = (name: string | null): string => {
  if (!name) return "?"
  return name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2)
}

export function ChatRoomCard({
  room,
  isActive = false,
  onClick,
  onLeave,
  onArchive,
}: ChatRoomCardProps) {
  const timeAgo = formatDistanceToNow(new Date(room.last_message_at), {
    addSuffix: true,
  })

  return (
    <div
      className={cn(
        "flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-colors hover:bg-accent",
        isActive && "bg-accent"
      )}
      onClick={onClick}
    >
      <Avatar className="size-12">
        <AvatarFallback className="bg-primary/10 text-primary">
          {room.type === ConversationType.DIRECT ? (
            getInitials(room.name)
          ) : (
            <Users className="size-5" />
          )}
        </AvatarFallback>
      </Avatar>

      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <h3 className="font-semibold text-sm truncate">
            {room.name || "Unnamed Room"}
          </h3>
          {room.type !== ConversationType.DIRECT && (
            <Badge variant="secondary" className="text-xs">
              {getConversationTypeLabel(room.type)}
            </Badge>
          )}
        </div>
        <div className="flex items-center gap-2">
          <p className="text-xs text-muted-foreground truncate flex-1">
            {room.description || "No description"}
          </p>
          {room.unread_count && room.unread_count > 0 && (
            <Badge variant="destructive" className="size-5 p-0 justify-center text-xs">
              {room.unread_count}
            </Badge>
          )}
        </div>
      </div>

      <div className="flex flex-col items-end gap-2">
        <span className="text-xs text-muted-foreground">{timeAgo}</span>
        <DropdownMenu>
          <DropdownMenuTrigger asChild onClick={(e) => e.stopPropagation()}>
            <Button variant="ghost" size="icon-sm">
              <MoreVertical className="size-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={(e) => {
              e.stopPropagation()
              onArchive?.()
            }}>
              <Archive className="size-4 mr-2" />
              Archive
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              className="text-destructive"
              onClick={(e) => {
                e.stopPropagation()
                onLeave?.()
              }}
            >
              <LogOut className="size-4 mr-2" />
              Leave Room
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  )
}
