import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import type { KeyboardEvent } from "react"
import { useEffect, useRef, useState } from "react"

import {
  createChat,
  createMessage,
  deleteChat,
  leaveChat,
  listChatContacts,
  listChats,
  listMessages,
  reportChat,
  type Chat,
  type ChatContact,
  type ChatsResponse,
  type Message,
  type MessagesResponse,
} from "@/client/chats.api"
import {
  ChatActionDialogs,
  ChatConversationPane,
  ChatListPane,
  NewChatDialog,
} from "@/components/Chats/ChatsPageSections"
import {
  appendMessage,
  getChatLabel,
  upsertChat,
} from "@/components/Chats/chats-utils"
import { useChatsRealtime } from "@/components/Chats/useChatsRealtime"
import useAuth from "@/hooks/useAuth"
import useCustomToast from "@/hooks/useCustomToast"

export const Route = createFileRoute("/_layout/chats")({
  component: ChatsPage,
})

function ChatsPage() {
  const queryClient = useQueryClient()
  const { user: currentUser } = useAuth()
  const { showErrorToast, showSuccessToast } = useCustomToast()
  const endRef = useRef<HTMLDivElement | null>(null)

  const [selectedChatId, setSelectedChatId] = useState<string | null>(null)
  const [isMobileView, setIsMobileView] = useState(() =>
    window.matchMedia("(max-width: 1023px)").matches,
  )
  const [chatSearch, setChatSearch] = useState("")
  const [contactSearch, setContactSearch] = useState("")
  const [selectedParticipantIds, setSelectedParticipantIds] = useState<string[]>(
    [],
  )
  const [messageText, setMessageText] = useState("")
  const [knownContacts, setKnownContacts] = useState<Record<string, ChatContact>>(
    {},
  )
  const [isNewChatOpen, setIsNewChatOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isLeaveDialogOpen, setIsLeaveDialogOpen] = useState(false)

  const {
    data: chatsData,
    isLoading: chatsLoading,
    error: chatsError,
  } = useQuery({
    queryKey: ["chats"],
    queryFn: listChats,
    refetchOnWindowFocus: true,
  })

  const {
    data: contacts = [],
    isLoading: contactsLoading,
    error: contactsError,
  } = useQuery({
    queryKey: ["chat-contacts", contactSearch],
    queryFn: () => listChatContacts(contactSearch),
    enabled: isNewChatOpen || !!selectedChatId,
  })

  const {
    data: messagesData,
    isLoading: messagesLoading,
    error: messagesError,
  } = useQuery({
    queryKey: ["messages", selectedChatId],
    queryFn: () => listMessages(selectedChatId as string),
    enabled: !!selectedChatId,
    refetchOnWindowFocus: true,
  })

  useEffect(() => {
    if (contacts.length === 0) return
    setKnownContacts((currentContacts) => {
      const nextContacts = { ...currentContacts }
      for (const contact of contacts) nextContacts[contact.id] = contact
      return nextContacts
    })
  }, [contacts])

  useEffect(() => {
    const mediaQuery = window.matchMedia("(max-width: 1023px)")
    const handleChange = (event: MediaQueryListEvent) => {
      setIsMobileView(event.matches)
    }

    setIsMobileView(mediaQuery.matches)
    mediaQuery.addEventListener("change", handleChange)
    return () => mediaQuery.removeEventListener("change", handleChange)
  }, [])

  const knownContactList = Object.values(knownContacts)
  const chats = chatsData?.data ?? []
  const messages = messagesData?.data ?? []

  useEffect(() => {
    if (chats.length === 0) {
      setSelectedChatId(null)
      return
    }

    const selectedStillExists = chats.some((chat) => chat.id === selectedChatId)
    if (selectedChatId && !selectedStillExists) {
      setSelectedChatId(isMobileView ? null : chats[0].id)
      return
    }

    if (!selectedChatId && !isMobileView) {
      setSelectedChatId(chats[0].id)
    }
  }, [chats, isMobileView, selectedChatId])

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" })
  }, [messages])

  const syncChatInCache = (chat: Chat) => {
    queryClient.setQueryData<ChatsResponse>(["chats"], (current) => ({
      data: upsertChat(current?.data ?? [], chat),
      count: current
        ? current.data.some((currentChat) => currentChat.id === chat.id)
          ? current.count
          : current.count + 1
        : 1,
    }))
  }

  const removeChatFromCache = (chatId: string) => {
    queryClient.setQueryData<ChatsResponse>(["chats"], (current) => {
      if (!current) return current
      const nextChats = current.data.filter((chat) => chat.id !== chatId)
      return {
        data: nextChats,
        count: nextChats.length,
      }
    })
    queryClient.removeQueries({ queryKey: ["messages", chatId] })
    setSelectedChatId((currentId) => (currentId === chatId ? null : currentId))
  }

  const syncMessageInCache = (chatId: string, message: Message) => {
    queryClient.setQueryData<MessagesResponse>(["messages", chatId], (current) => ({
      data: appendMessage(current?.data ?? [], message),
      count: current?.data.some((currentMessage) => currentMessage.id === message.id)
        ? current.count
        : (current?.count ?? 0) + 1,
    }))
  }

  useChatsRealtime({
    currentUserId: currentUser?.id,
    queryClient,
    onChatRemoved: (chatId) => {
      setSelectedChatId((currentId) => (currentId === chatId ? null : currentId))
    },
  })

  const createChatMutation = useMutation({
    mutationFn: () => createChat({ participants: selectedParticipantIds }),
    onSuccess: (chat) => {
      showSuccessToast("Conversation created")
      setSelectedParticipantIds([])
      setContactSearch("")
      setIsNewChatOpen(false)
      setSelectedChatId(chat.id)
      syncChatInCache(chat)
    },
    onError: (error) => {
      showErrorToast(error instanceof Error ? error.message : "Failed to create chat")
    },
  })

  const selectedChat = chats.find((chat) => chat.id === selectedChatId) ?? null

  const sendMessageMutation = useMutation({
    mutationFn: () =>
      createMessage(selectedChatId as string, {
        content: messageText.trim(),
        attachments: [],
      }),
    onSuccess: (message) => {
      setMessageText("")
      if (!selectedChatId || !selectedChat) return
      syncMessageInCache(selectedChatId, message)
      syncChatInCache({
        ...selectedChat,
        last_message: message.content,
        updated_at: message.created_at,
      })
    },
    onError: (error) => {
      showErrorToast(error instanceof Error ? error.message : "Failed to send message")
    },
  })

  const deleteChatMutation = useMutation({
    mutationFn: (chatId: string) => deleteChat(chatId),
    onSuccess: (_, deletedChatId) => {
      showSuccessToast("Conversation deleted")
      setIsDeleteDialogOpen(false)
      setMessageText("")
      removeChatFromCache(deletedChatId)
    },
    onError: (error) => {
      showErrorToast(error instanceof Error ? error.message : "Failed to delete chat")
    },
  })

  const leaveChatMutation = useMutation({
    mutationFn: (chatId: string) => leaveChat(chatId),
    onSuccess: (_, leftChatId) => {
      showSuccessToast("You left the conversation")
      setIsLeaveDialogOpen(false)
      setMessageText("")
      removeChatFromCache(leftChatId)
    },
    onError: (error) => {
      showErrorToast(error instanceof Error ? error.message : "Failed to leave chat")
    },
  })

  const reportChatMutation = useMutation({
    mutationFn: (chatId: string) => reportChat(chatId),
    onSuccess: () => {
      showSuccessToast("Conversation reported")
    },
    onError: (error) => {
      showErrorToast(error instanceof Error ? error.message : "Failed to report chat")
    },
  })

  const filteredChats = chats.filter((chat) => {
    const query = chatSearch.trim().toLowerCase()
    if (!query) return true

    const label = getChatLabel(chat, currentUser?.id, knownContactList).toLowerCase()
    return [label, chat.last_message || ""].some((value) =>
      value.toLowerCase().includes(query),
    )
  })

  const selectedContacts = selectedParticipantIds
    .map((participantId) => knownContacts[participantId])
    .filter((contact): contact is ChatContact => Boolean(contact))

  const participantContacts = selectedChat
    ? selectedChat.participants
        .filter((participantId) => participantId !== currentUser?.id)
        .map((participantId) => knownContacts[participantId])
        .filter((contact): contact is ChatContact => Boolean(contact))
    : []

  const selectedChatLabel = getChatLabel(
    selectedChat,
    currentUser?.id,
    knownContactList,
  )

  const toggleParticipant = (participantId: string) => {
    setSelectedParticipantIds((currentIds) =>
      currentIds.includes(participantId)
        ? currentIds.filter((id) => id !== participantId)
        : [...currentIds, participantId],
    )
  }

  const handleSendMessage = () => {
    if (!selectedChatId || !messageText.trim() || sendMessageMutation.isPending) return
    sendMessageMutation.mutate()
  }

  const handleComposerKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="min-h-[calc(100vh-5rem)] bg-[linear-gradient(180deg,rgba(15,23,42,0.04),transparent),radial-gradient(circle_at_top_left,rgba(13,148,136,0.08),transparent_32%)] px-3 py-3 md:px-6 md:py-6">
      <NewChatDialog
        open={isNewChatOpen}
        onOpenChange={setIsNewChatOpen}
        contactSearch={contactSearch}
        onContactSearchChange={setContactSearch}
        selectedContacts={selectedContacts}
        selectedParticipantIds={selectedParticipantIds}
        contacts={contacts}
        contactsLoading={contactsLoading}
        contactsError={contactsError}
        onToggleParticipant={toggleParticipant}
        onCreateChat={() => createChatMutation.mutate()}
        isCreatingChat={createChatMutation.isPending}
      />

      <ChatActionDialogs
        isDeleteDialogOpen={isDeleteDialogOpen}
        onDeleteDialogOpenChange={setIsDeleteDialogOpen}
        isDeletePending={deleteChatMutation.isPending}
        onDelete={() => selectedChatId && deleteChatMutation.mutate(selectedChatId)}
        isLeaveDialogOpen={isLeaveDialogOpen}
        onLeaveDialogOpenChange={setIsLeaveDialogOpen}
        isLeavePending={leaveChatMutation.isPending}
        onLeave={() => selectedChatId && leaveChatMutation.mutate(selectedChatId)}
      />

      <div className="mx-auto flex h-[calc(100vh-6.4rem)] max-w-7xl overflow-hidden rounded-[32px] border border-border/60 bg-card shadow-[0_30px_80px_-40px_rgba(15,23,42,0.55)]">
        <ChatListPane
          chats={chats}
          filteredChats={filteredChats}
          selectedChatId={selectedChatId}
          currentUserId={currentUser?.id}
          knownContacts={knownContactList}
          chatSearch={chatSearch}
          onChatSearchChange={setChatSearch}
          onSelectChat={setSelectedChatId}
          onOpenNewChat={() => setIsNewChatOpen(true)}
          chatsLoading={chatsLoading}
          chatsError={chatsError}
          isMobileConversationOpen={Boolean(selectedChatId)}
        />

        <ChatConversationPane
          selectedChat={selectedChat}
          selectedChatId={selectedChatId}
          selectedChatLabel={selectedChatLabel}
          participantContacts={participantContacts}
          messages={messages}
          currentUserId={currentUser?.id}
          messageText={messageText}
          onMessageTextChange={setMessageText}
          onComposerKeyDown={handleComposerKeyDown}
          onSendMessage={handleSendMessage}
          onBack={() => setSelectedChatId(null)}
          onOpenDeleteDialog={() => setIsDeleteDialogOpen(true)}
          onOpenLeaveDialog={() => setIsLeaveDialogOpen(true)}
          onReportChat={(chatId) => reportChatMutation.mutate(chatId)}
          messagesLoading={messagesLoading}
          messagesError={messagesError}
          isSendPending={sendMessageMutation.isPending}
          endRef={endRef}
          isMobileConversationOpen={Boolean(selectedChatId)}
        />
      </div>
    </div>
  )
}
