import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useCreateRoom } from "@/hooks/useChat"
import { ConversationType, type RoomCreate } from "@/types/chat"

interface CreateRoomDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function CreateRoomDialog({ open, onOpenChange }: CreateRoomDialogProps) {
  const [name, setName] = useState("")
  const [description, setDescription] = useState("")
  const [type, setType] = useState<ConversationType>(ConversationType.GROUP)
  const [apiError, setApiError] = useState<string | null>(null)
  
  const createRoomMutation = useCreateRoom()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    const roomData: RoomCreate = {
      name,
      description: description || null,
      type,
    }

    ;(async () => {
      try {
        await createRoomMutation.mutateAsync(roomData)
        onOpenChange(false)
        setName("")
        setDescription("")
        setType(ConversationType.GROUP)
        setApiError(null)
      } catch (err: any) {
        // show error message inline for debugging
        const message = err?.response?.data?.detail || err?.message || "Failed to create room"
        setApiError(String(message))
        console.error("Create room error:", err)
      }
    })()
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>Create New Room</DialogTitle>
            <DialogDescription>
              Start a new conversation with your team
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="room-type">Room Type</Label>
              <Select
                value={type.toString()}
                onValueChange={(value) => setType(Number(value) as ConversationType)}
              >
                <SelectTrigger id="room-type">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value={ConversationType.DIRECT.toString()}>
                    Direct Message
                  </SelectItem>
                  <SelectItem value={ConversationType.GROUP.toString()}>
                    Group Chat
                  </SelectItem>
                  <SelectItem value={ConversationType.MENTORSHIP.toString()}>
                    Mentorship
                  </SelectItem>
                  <SelectItem value={ConversationType.RESEARCH.toString()}>
                    Research Group
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="room-name">Room Name</Label>
              <Input
                id="room-name"
                placeholder="Enter room name..."
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="room-description">Description (Optional)</Label>
              <Textarea
                id="room-description"
                placeholder="Enter room description..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
              />
            </div>
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
            >
              Cancel
            </Button>
            <div className="flex flex-col items-end gap-2">
              {apiError && (
                <div className="text-sm text-destructive">{apiError}</div>
              )}
              <Button
                type="submit"
                disabled={!name.trim() || createRoomMutation.isPending}
              >
                {createRoomMutation.isPending ? "Creating..." : "Create Room"}
              </Button>
            </div>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
