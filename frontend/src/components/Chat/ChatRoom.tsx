import { useEffect, useRef, useState } from "react"
import { MoreVertical, Users, Phone, Video } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Skeleton } from "@/components/ui/skeleton"
import { MessageBubble } from "./MessageBubble"
import { MessageInput } from "./MessageInput"
import {
  useMessages,
  useSendMessage,
  useDeleteMessage,
  useAddReaction,
} from "@/hooks/useChat"
import useAuth from "@/hooks/useAuth"
import type { RoomPublic, MessageCreate } from "@/types/chat"

interface ChatRoomProps {
  room: RoomPublic
  onViewMembers?: () => void
  onRoomSettings?: () => void
}

export function ChatRoom({ room, onViewMembers, onRoomSettings }: ChatRoomProps) {
  const { user } = useAuth()
  const { data: messagesData, isLoading } = useMessages(room.id)
  const sendMessageMutation = useSendMessage()
  const deleteMessageMutation = useDeleteMessage()
  const addReactionMutation = useAddReaction()

  const [replyTo, setReplyTo] = useState<{
    id: string
    content: string
  } | null>(null)

  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messagesData?.data])

  const handleSendMessage = (content: string) => {
    const messageData: MessageCreate = {
      room_id: room.id,
      content,
      reply_to_id: replyTo?.id || null,
    }

    sendMessageMutation.mutate(messageData, {
      onSuccess: () => {
        setReplyTo(null)
      },
    })
  }

  const handleDeleteMessage = (messageId: string) => {
    if (confirm("Are you sure you want to delete this message?")) {
      deleteMessageMutation.mutate({ messageId, roomId: room.id })
    }
  }

  const handleReact = (messageId: string, emoji: string) => {
    addReactionMutation.mutate({
      data: { message_id: messageId, emoji },
      roomId: room.id,
    })
  }

  if (isLoading) {
    return (
      <div className="flex flex-col h-full">
        <div className="flex items-center justify-between p-4 border-b">
          <Skeleton className="h-6 w-48" />
          <Skeleton className="h-9 w-9 rounded-full" />
        </div>
        <div className="flex-1 p-4 space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="flex gap-2">
              <Skeleton className="size-8 rounded-full" />
              <Skeleton className="h-16 flex-1 max-w-md rounded-lg" />
            </div>
          ))}
        </div>
        <Skeleton className="h-24 m-4" />
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full bg-background">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b">
        <div className="flex items-center gap-3">
          <div>
            <h2 className="text-lg font-semibold">
              {room.name || "Unnamed Room"}
            </h2>
            <p className="text-sm text-muted-foreground">
              {room.member_count ? `${room.member_count} members` : ""}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" disabled>
            <Phone className="size-5" />
          </Button>
          <Button variant="ghost" size="icon" disabled>
            <Video className="size-5" />
          </Button>
          <Button variant="ghost" size="icon" onClick={onViewMembers}>
            <Users className="size-5" />
          </Button>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon">
                <MoreVertical className="size-5" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={onViewMembers}>
                View Members
              </DropdownMenuItem>
              <DropdownMenuItem onClick={onRoomSettings}>
                Room Settings
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem className="text-destructive">
                Leave Room
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      {/* Messages */}
      <ScrollArea className="flex-1 p-4" ref={scrollAreaRef}>
        {messagesData?.data && messagesData.data.length > 0 ? (
          <>
            {messagesData.data.map((message) => (
              <MessageBubble
                key={message.id}
                message={message}
                isOwn={message.sender_id === user?.id}
                onDelete={() => handleDeleteMessage(message.id)}
                onReact={(emoji) => handleReact(message.id, emoji)}
                onReply={() =>
                  setReplyTo({
                    id: message.id,
                    content: message.content,
                  })
                }
              />
            ))}
            <div ref={messagesEndRef} />
          </>
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <p className="text-muted-foreground">No messages yet</p>
            <p className="text-sm text-muted-foreground mt-1">
              Be the first to send a message
            </p>
          </div>
        )}
      </ScrollArea>

      {/* Message Input */}
      <MessageInput
        onSend={handleSendMessage}
        replyTo={replyTo}
        onCancelReply={() => setReplyTo(null)}
        disabled={sendMessageMutation.isPending}
      />
    </div>
  )
}
