import { Search, Plus } from "lucide-react"
import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { ChatRoomCard } from "./ChatRoomCard"
import { useRooms, useLeaveRoom, useUpdateRoom } from "@/hooks/useChat"
import { Skeleton } from "@/components/ui/skeleton"
import type { RoomPublic } from "@/types/chat"

interface ChatListProps {
  activeRoomId?: string | null
  onRoomSelect?: (room: RoomPublic) => void
  onCreateRoom?: () => void
}

export function ChatList({ activeRoomId, onRoomSelect, onCreateRoom }: ChatListProps) {
  const [searchQuery, setSearchQuery] = useState("")
  const { data: rooms, isLoading } = useRooms()
  const leaveRoomMutation = useLeaveRoom()
  const updateRoomMutation = useUpdateRoom()

  const filteredRooms = (rooms?.data ?? []).filter((room) =>
    (room.name || "").toLowerCase().includes(searchQuery.toLowerCase()) ||
    (room.description || "").toLowerCase().includes(searchQuery.toLowerCase())
  )

  const handleLeaveRoom = (roomId: string) => {
    if (confirm("Are you sure you want to leave this room?")) {
      leaveRoomMutation.mutate(roomId)
    }
  }

  const handleArchiveRoom = (roomId: string) => {
    updateRoomMutation.mutate({
      roomId,
      data: { is_archived: true },
    })
  }

  if (isLoading) {
    return (
      <div className="flex flex-col h-full border-r">
        <div className="p-4 border-b space-y-4">
          <Skeleton className="h-10 w-full" />
          <Skeleton className="h-10 w-full" />
        </div>
        <div className="flex-1 p-4 space-y-3">
          {[...Array(5)].map((_, i) => (
            <Skeleton key={i} className="h-16 w-full" />
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full border-r bg-background">
      {/* Header */}
      <div className="p-4 border-b space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Messages</h2>
          <Button size="icon-sm" onClick={onCreateRoom}>
            <Plus className="size-4" />
          </Button>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" />
          <Input
            placeholder="Search conversations..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9"
          />
        </div>
      </div>

      {/* Room List */}
      <ScrollArea className="flex-1">
        <div className="p-2 space-y-1">
          {filteredRooms && filteredRooms.length > 0 ? (
            filteredRooms.map((room) => (
              <ChatRoomCard
                key={room.id}
                room={room}
                isActive={room.id === activeRoomId}
                onClick={() => onRoomSelect?.(room)}
                onLeave={() => handleLeaveRoom(room.id)}
                onArchive={() => handleArchiveRoom(room.id)}
              />
            ))
          ) : (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <p className="text-muted-foreground">
                {searchQuery ? "No rooms found" : "No conversations yet"}
              </p>
              <Button
                variant="link"
                className="mt-2"
                onClick={onCreateRoom}
              >
                Start a conversation
              </Button>
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  )
}
