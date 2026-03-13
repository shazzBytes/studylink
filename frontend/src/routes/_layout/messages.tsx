import { useState } from "react"
import { createFileRoute } from "@tanstack/react-router"
import { MessageSquare } from "lucide-react"
import { ChatList } from "@/components/Chat/ChatList"
import { ChatRoom } from "@/components/Chat/ChatRoom"
import { CreateRoomDialog } from "@/components/Chat/CreateRoomDialog"
import type { RoomPublic } from "@/types/chat"

export const Route = createFileRoute("/_layout/messages")({
  component: MessagesPage,
})

function MessagesPage() {
  const [selectedRoom, setSelectedRoom] = useState<RoomPublic | null>(null)
  const [isCreateRoomOpen, setIsCreateRoomOpen] = useState(false)

  return (
    <div className="flex h-[calc(100vh-64px)]">
      {/* Chat List Sidebar */}
      <div className="w-80 flex-shrink-0">
        <ChatList
          activeRoomId={selectedRoom?.id}
          onRoomSelect={setSelectedRoom}
          onCreateRoom={() => setIsCreateRoomOpen(true)}
        />
      </div>

      {/* Chat Room Area */}
      <div className="flex-1">
        {selectedRoom ? (
          <ChatRoom room={selectedRoom} />
        ) : (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="rounded-full bg-muted p-6 mb-4">
              <MessageSquare className="size-12 text-muted-foreground" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Select a conversation</h3>
            <p className="text-muted-foreground max-w-sm">
              Choose a conversation from the list to start messaging, or create a new
              room to begin.
            </p>
          </div>
        )}
      </div>

      {/* Create Room Dialog */}
      <CreateRoomDialog
        open={isCreateRoomOpen}
        onOpenChange={setIsCreateRoomOpen}
      />
    </div>
  )
}
