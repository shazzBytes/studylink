import { formatDistanceToNow } from "date-fns"
import { Check, CheckCheck, MoreVertical, Reply, Smile } from "lucide-react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { cn } from "@/lib/utils"
import type { MessagePublic } from "@/types/chat"
import { MessageStatus } from "@/types/chat"

interface MessageBubbleProps {
  message: MessagePublic
  isOwn: boolean
  onEdit?: () => void
  onDelete?: () => void
  onReact?: (emoji: string) => void
  onReply?: () => void
}

const getInitials = (name: string | null | undefined): string => {
  if (!name) return "?"
  return name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2)
}

const MessageStatusIcon = ({ status }: { status: MessageStatus }) => {
  switch (status) {
    case MessageStatus.SENT:
      return <Check className="size-3" />
    case MessageStatus.DELIVERED:
      return <CheckCheck className="size-3" />
    case MessageStatus.READ:
      return <CheckCheck className="size-3 text-primary" />
    default:
      return null
  }
}

export function MessageBubble({
  message,
  isOwn,
  onEdit,
  onDelete,
  onReact,
  onReply,
}: MessageBubbleProps) {
  const [showActions, setShowActions] = useState(false)
  const timeAgo = formatDistanceToNow(new Date(message.created_at), {
    addSuffix: true,
  })

  if (message.is_deleted) {
    return (
      <div className={cn("flex gap-2 mb-4", isOwn && "flex-row-reverse")}>
        <div className="flex-1" />
        <div className="max-w-[70%] px-4 py-2 rounded-lg bg-muted/50 italic text-muted-foreground text-sm">
          This message was deleted
        </div>
      </div>
    )
  }

  return (
    <div
      className={cn("flex gap-2 mb-4 group", isOwn && "flex-row-reverse")}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      {!isOwn && (
        <Avatar className="size-8">
          <AvatarFallback className="text-xs">
            {getInitials(message.sender_name)}
          </AvatarFallback>
        </Avatar>
      )}

      <div className={cn("flex flex-col gap-1 max-w-[70%]", isOwn && "items-end")}>
        {!isOwn && (
          <span className="text-xs font-medium text-muted-foreground px-3">
            {message.sender_name || "Unknown"}
          </span>
        )}

        <div
          className={cn(
            "relative px-4 py-2 rounded-lg",
            isOwn
              ? "bg-primary text-primary-foreground"
              : "bg-muted"
          )}
        >
          <p className="text-sm whitespace-pre-wrap break-words">
            {message.content}
          </p>

          {message.is_edited && (
            <span className="text-xs opacity-70 ml-2">(edited)</span>
          )}

          <div className={cn(
            "flex items-center gap-1 mt-1",
            isOwn ? "justify-end" : "justify-start"
          )}>
            <span className="text-xs opacity-70">{timeAgo}</span>
            {isOwn && <MessageStatusIcon status={message.status} />}
          </div>

          {/* Reactions */}
          {message.reaction_count && message.reaction_count > 0 && (
            <div className="absolute -bottom-2 right-2 flex gap-1 px-2 py-0.5 bg-background border rounded-full shadow-sm">
              <Smile className="size-3" />
              <span className="text-xs">{message.reaction_count}</span>
            </div>
          )}
        </div>

        {/* Action buttons */}
        {showActions && (
          <div className={cn(
            "flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity",
            isOwn && "flex-row-reverse"
          )}>
            <Button
              variant="ghost"
              size="icon-sm"
              onClick={() => onReact?.("👍")}
            >
              <Smile className="size-3" />
            </Button>
            <Button
              variant="ghost"
              size="icon-sm"
              onClick={onReply}
            >
              <Reply className="size-3" />
            </Button>
            {isOwn && (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="icon-sm">
                    <MoreVertical className="size-3" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align={isOwn ? "end" : "start"}>
                  <DropdownMenuItem onClick={onEdit}>
                    Edit
                  </DropdownMenuItem>
                  <DropdownMenuItem
                    className="text-destructive"
                    onClick={onDelete}
                  >
                    Delete
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
