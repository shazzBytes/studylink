import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { useEffect, useMemo, useState } from "react"
import {
  createChat,
  createMessage,
  listChats,
  listMessages,
  type Message,
} from "@/client/chats.api"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Skeleton } from "@/components/ui/skeleton"
import { Textarea } from "@/components/ui/textarea"
import useCustomToast from "@/hooks/useCustomToast"
import { getInitials } from "@/utils"

export const Route = createFileRoute("/_layout/chats")({
  component: ChatsPage,
})

function ChatsPage() {
  const queryClient = useQueryClient()
  const { showErrorToast, showSuccessToast } = useCustomToast()

  const [selectedChatId, setSelectedChatId] = useState<string | null>(null)
  const [newChatTitle, setNewChatTitle] = useState("")
  const [messageText, setMessageText] = useState("")

  const {
    data: chatsData,
    isLoading: chatsLoading,
    error: chatsError,
  } = useQuery({
    queryKey: ["chats"],
    queryFn: listChats,
  })

  const chats = chatsData?.data || []

  useEffect(() => {
    if (!selectedChatId && chats.length > 0) {
      setSelectedChatId(chats[0].id)
    }
  }, [chats, selectedChatId])

  const selectedChat = useMemo(
    () => chats.find((chat) => chat.id === selectedChatId) || null,
    [chats, selectedChatId],
  )

  const {
    data: messagesData,
    isLoading: messagesLoading,
    error: messagesError,
  } = useQuery({
    queryKey: ["messages", selectedChatId],
    queryFn: () => listMessages(selectedChatId as string),
    enabled: !!selectedChatId,
  })

  const messages = messagesData?.data || []

  const createChatMutation = useMutation({
    mutationFn: () => createChat({ title: newChatTitle.trim() || "New chat" }),
    onSuccess: (chat) => {
      showSuccessToast("Chat created")
      setNewChatTitle("")
      setSelectedChatId(chat.id)
      queryClient.invalidateQueries({ queryKey: ["chats"] })
    },
    onError: (error) => {
      showErrorToast(error instanceof Error ? error.message : "Failed to create chat")
    },
  })

  const sendMessageMutation = useMutation({
    mutationFn: () =>
      createMessage(selectedChatId as string, {
        content: messageText.trim(),
        attachments: [],
      }),
    onSuccess: () => {
      setMessageText("")
      queryClient.invalidateQueries({ queryKey: ["messages", selectedChatId] })
      queryClient.invalidateQueries({ queryKey: ["chats"] })
    },
    onError: (error) => {
      showErrorToast(error instanceof Error ? error.message : "Failed to send message")
    },
  })

  const handleCreateChat = () => {
    if (createChatMutation.isPending) return
    createChatMutation.mutate()
  }

  const handleSendMessage = () => {
    if (!selectedChatId || !messageText.trim() || sendMessageMutation.isPending) return
    sendMessageMutation.mutate()
  }

  return (
    <div className="container mx-auto h-[calc(100vh-8rem)] max-w-7xl p-4 md:p-6">
      <div className="grid h-full gap-4 md:grid-cols-[320px_1fr]">
        <Card className="flex h-full flex-col">
          <CardHeader className="space-y-3">
            <CardTitle>Chats</CardTitle>
            <div className="flex gap-2">
              <Input
                placeholder="New chat title"
                value={newChatTitle}
                onChange={(e) => setNewChatTitle(e.target.value)}
              />
              <Button
                onClick={handleCreateChat}
                disabled={createChatMutation.isPending}
              >
                New
              </Button>
            </div>
          </CardHeader>
          <CardContent className="min-h-0 flex-1 p-0">
            <ScrollArea className="h-full">
              <div className="space-y-2 p-3">
                {chatsLoading ? (
                  Array.from({ length: 5 }).map((_, idx) => (
                    <Skeleton key={idx} className="h-16 w-full" />
                  ))
                ) : chatsError ? (
                  <p className="text-sm text-destructive">
                    {chatsError instanceof Error
                      ? chatsError.message
                      : "Failed to load chats"}
                  </p>
                ) : chats.length === 0 ? (
                  <p className="text-sm text-muted-foreground">No chats yet</p>
                ) : (
                  chats.map((chat) => (
                    <button
                      key={chat.id}
                      type="button"
                      onClick={() => setSelectedChatId(chat.id)}
                      className={`w-full rounded-lg border p-3 text-left transition ${
                        selectedChatId === chat.id
                          ? "border-primary bg-primary/5"
                          : "hover:bg-muted/60"
                      }`}
                    >
                      <p className="truncate font-medium">
                        {chat.title || "Untitled chat"}
                      </p>
                      <p className="truncate text-xs text-muted-foreground">
                        {chat.last_message || "No messages yet"}
                      </p>
                    </button>
                  ))
                )}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>

        <Card className="flex h-full flex-col">
          <CardHeader>
            <CardTitle>{selectedChat?.title || "Select a chat"}</CardTitle>
          </CardHeader>
          <CardContent className="flex min-h-0 flex-1 flex-col gap-3">
            <ScrollArea className="flex-1 rounded-md border">
              <div className="space-y-3 p-4">
                {selectedChatId ? (
                  messagesLoading ? (
                    Array.from({ length: 4 }).map((_, idx) => (
                      <Skeleton key={idx} className="h-14 w-full" />
                    ))
                  ) : messagesError ? (
                    <p className="text-sm text-destructive">
                      {messagesError instanceof Error
                        ? messagesError.message
                        : "Failed to load messages"}
                    </p>
                  ) : messages.length === 0 ? (
                    <p className="text-sm text-muted-foreground">
                      Start the conversation by sending a message.
                    </p>
                  ) : (
                    messages.map((message: Message) => (
                      <div key={message.id} className="flex items-start gap-3">
                        <Avatar className="h-8 w-8">
                          <AvatarFallback className="text-xs">
                            {getInitials(message.sender_id)}
                          </AvatarFallback>
                        </Avatar>
                        <div className="max-w-[85%] rounded-lg bg-muted p-3">
                          <p className="text-sm">{message.content}</p>
                          <p className="mt-1 text-xs text-muted-foreground">
                            {message.created_at
                              ? new Date(message.created_at).toLocaleString()
                              : "Just now"}
                          </p>
                        </div>
                      </div>
                    ))
                  )
                ) : (
                  <p className="text-sm text-muted-foreground">
                    Select a chat from the left panel.
                  </p>
                )}
              </div>
            </ScrollArea>

            <div className="flex gap-2">
              <Textarea
                placeholder="Write a message..."
                value={messageText}
                onChange={(e) => setMessageText(e.target.value)}
                className="min-h-12"
                disabled={!selectedChatId}
              />
              <Button
                onClick={handleSendMessage}
                disabled={!selectedChatId || !messageText.trim() || sendMessageMutation.isPending}
              >
                Send
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
