import type { KeyboardEvent, ReactNode } from "react"
import {
  ArrowLeft,
  Check,
  Flag,
  MoreHorizontal,
  Search,
  SendHorizontal,
  SquarePen,
  Trash2,
  User,
  UserRoundMinus,
  Users,
  X,
} from "lucide-react"

import type { Chat, ChatContact, Message } from "@/client/chats.api"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Skeleton } from "@/components/ui/skeleton"
import { Textarea } from "@/components/ui/textarea"
import { cn } from "@/lib/utils"
import { getInitials } from "@/utils"

import {
  formatTimestamp,
  getChatLabel,
  getChatTypeLabel,
  getContactLabel,
} from "./chats-utils"

export function EmptyState({
  title,
  description,
  icon,
}: {
  title: string
  description: string
  icon?: ReactNode
}) {
  return (
    <div className="flex h-full items-center justify-center px-6 py-12">
      <div className="max-w-sm text-center">
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-3xl bg-primary/10 text-primary">
          {icon ?? <Users className="h-6 w-6" />}
        </div>
        <h3 className="mt-4 text-xl font-semibold">{title}</h3>
        <p className="mt-2 text-sm leading-6 text-muted-foreground">
          {description}
        </p>
      </div>
    </div>
  )
}

export function NewChatDialog({
  open,
  onOpenChange,
  contactSearch,
  onContactSearchChange,
  selectedContacts,
  selectedParticipantIds,
  contacts,
  contactsLoading,
  contactsError,
  onToggleParticipant,
  onCreateChat,
  isCreatingChat,
}: {
  open: boolean
  onOpenChange: (open: boolean) => void
  contactSearch: string
  onContactSearchChange: (value: string) => void
  selectedContacts: ChatContact[]
  selectedParticipantIds: string[]
  contacts: ChatContact[]
  contactsLoading: boolean
  contactsError: unknown
  onToggleParticipant: (participantId: string) => void
  onCreateChat: () => void
  isCreatingChat: boolean
}) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-xl rounded-[28px] border-border/70 p-0">
        <DialogHeader className="border-b border-border/60 px-6 py-5">
          <DialogTitle>New conversation</DialogTitle>
          <DialogDescription>
            Choose one or more people to start chatting with.
          </DialogDescription>
        </DialogHeader>

        <div className="px-6 py-4">
          <div className="relative">
            <Search className="text-muted-foreground absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2" />
            <Input
              value={contactSearch}
              onChange={(event) => onContactSearchChange(event.target.value)}
              placeholder="Search people"
              className="h-11 rounded-2xl pl-9"
            />
          </div>

          {selectedContacts.length > 0 ? (
            <div className="mt-4 flex flex-wrap gap-2">
              {selectedContacts.map((contact) => (
                <button
                  key={contact.id}
                  type="button"
                  onClick={() => onToggleParticipant(contact.id)}
                  className="inline-flex items-center gap-2 rounded-full bg-primary/10 px-3 py-1.5 text-sm text-primary"
                >
                  <span>{getContactLabel(contact)}</span>
                  <X className="h-3.5 w-3.5" />
                </button>
              ))}
            </div>
          ) : null}

          <ScrollArea className="mt-4 h-80 rounded-[24px] border border-border/70 bg-muted/20">
            <div className="space-y-1 p-2">
              {contactsLoading ? (
                Array.from({ length: 6 }).map((_, idx) => (
                  <Skeleton key={idx} className="h-14 w-full rounded-2xl" />
                ))
              ) : contactsError ? (
                <p className="p-3 text-sm text-destructive">
                  {contactsError instanceof Error
                    ? contactsError.message
                    : "Failed to load people"}
                </p>
              ) : contacts.length === 0 ? (
                <p className="p-3 text-sm text-muted-foreground">No people found.</p>
              ) : (
                contacts.map((contact) => {
                  const isSelected = selectedParticipantIds.includes(contact.id)
                  return (
                    <button
                      key={contact.id}
                      type="button"
                      onClick={() => onToggleParticipant(contact.id)}
                      className={cn(
                        "flex w-full items-center gap-3 rounded-2xl px-3 py-3 text-left transition",
                        isSelected ? "bg-primary/10" : "hover:bg-background",
                      )}
                    >
                      <Avatar className="h-10 w-10">
                        <AvatarFallback>{getInitials(getContactLabel(contact))}</AvatarFallback>
                      </Avatar>
                      <div className="min-w-0 flex-1">
                        <p className="truncate text-sm font-medium">
                          {getContactLabel(contact)}
                        </p>
                        <p className="truncate text-xs text-muted-foreground">
                          {contact.email}
                        </p>
                      </div>
                      <div
                        className={cn(
                          "flex h-6 w-6 items-center justify-center rounded-full border",
                          isSelected
                            ? "border-primary bg-primary text-primary-foreground"
                            : "border-border",
                        )}
                      >
                        {isSelected ? <Check className="h-3.5 w-3.5" /> : null}
                      </div>
                    </button>
                  )
                })
              )}
            </div>
          </ScrollArea>
        </div>

        <DialogFooter className="border-t border-border/60 px-6 py-4">
          <Button
            variant="outline"
            onClick={() => onOpenChange(false)}
            disabled={isCreatingChat}
          >
            Cancel
          </Button>
          <Button
            onClick={onCreateChat}
            disabled={selectedParticipantIds.length === 0 || isCreatingChat}
          >
            Start conversation
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

export function ChatActionDialogs({
  isDeleteDialogOpen,
  onDeleteDialogOpenChange,
  isDeletePending,
  onDelete,
  isLeaveDialogOpen,
  onLeaveDialogOpenChange,
  isLeavePending,
  onLeave,
}: {
  isDeleteDialogOpen: boolean
  onDeleteDialogOpenChange: (open: boolean) => void
  isDeletePending: boolean
  onDelete: () => void
  isLeaveDialogOpen: boolean
  onLeaveDialogOpenChange: (open: boolean) => void
  isLeavePending: boolean
  onLeave: () => void
}) {
  return (
    <>
      <AlertDialog open={isDeleteDialogOpen} onOpenChange={onDeleteDialogOpenChange}>
        <AlertDialogContent className="rounded-[28px]">
          <AlertDialogHeader>
            <AlertDialogTitle>Delete this conversation?</AlertDialogTitle>
            <AlertDialogDescription>
              This removes the conversation for everyone who still has access to it.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={isDeletePending}>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={onDelete}
              disabled={isDeletePending}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Delete chat
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      <AlertDialog open={isLeaveDialogOpen} onOpenChange={onLeaveDialogOpenChange}>
        <AlertDialogContent className="rounded-[28px]">
          <AlertDialogHeader>
            <AlertDialogTitle>Leave this conversation?</AlertDialogTitle>
            <AlertDialogDescription>
              You will stop receiving messages. If you are added back later, you
              will only see messages from the new join time onward.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={isLeavePending}>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={onLeave}
              disabled={isLeavePending}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Leave chat
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  )
}

export function ChatListPane({
  chats,
  filteredChats,
  selectedChatId,
  currentUserId,
  knownContacts,
  chatSearch,
  onChatSearchChange,
  onSelectChat,
  onOpenNewChat,
  chatsLoading,
  chatsError,
  isMobileConversationOpen,
}: {
  chats: Chat[]
  filteredChats: Chat[]
  selectedChatId: string | null
  currentUserId?: string
  knownContacts: ChatContact[]
  chatSearch: string
  onChatSearchChange: (value: string) => void
  onSelectChat: (chatId: string) => void
  onOpenNewChat: () => void
  chatsLoading: boolean
  chatsError: unknown
  isMobileConversationOpen: boolean
}) {
  return (
    <aside
      className={cn(
        "flex w-full min-w-0 flex-col border-r border-border/60 bg-background/80 lg:w-[360px] lg:flex-none",
        isMobileConversationOpen ? "hidden lg:flex" : "flex",
      )}
    >
      <div className="border-b border-border/60 px-5 py-5">
        <div className="flex items-center justify-between gap-3">
          <div>
            <h1 className="text-2xl font-semibold">Chats</h1>
            <p className="mt-1 text-sm text-muted-foreground">
              Direct messages and group threads
            </p>
          </div>
          <Button size="icon" className="h-11 w-11 rounded-2xl" onClick={onOpenNewChat}>
            <SquarePen className="h-4 w-4" />
          </Button>
        </div>

        <div className="relative mt-4">
          <Search className="text-muted-foreground absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2" />
          <Input
            value={chatSearch}
            onChange={(event) => onChatSearchChange(event.target.value)}
            placeholder="Search chats"
            className="h-11 rounded-2xl bg-background pl-9"
          />
        </div>
      </div>

      <ScrollArea className="min-h-0 flex-1">
        <div className="space-y-1 p-3">
          {chatsLoading ? (
            Array.from({ length: 8 }).map((_, idx) => (
              <Skeleton key={idx} className="h-18 w-full rounded-3xl" />
            ))
          ) : chatsError ? (
            <div className="rounded-3xl border border-destructive/20 bg-destructive/5 px-4 py-3 text-sm text-destructive">
              {chatsError instanceof Error
                ? chatsError.message
                : "Failed to load chats"}
            </div>
          ) : filteredChats.length === 0 ? (
            <EmptyState
              title={chats.length === 0 ? "No conversations yet" : "No matching chats"}
              description={
                chats.length === 0
                  ? "Start a new conversation to populate your inbox."
                  : "Try another search term."
              }
            />
          ) : (
            filteredChats.map((chat) => {
              const label = getChatLabel(chat, currentUserId, knownContacts)
              const isActive = selectedChatId === chat.id
              const ChatIcon = chat.chat_type === "group" ? Users : User
              return (
                <button
                  key={chat.id}
                  type="button"
                  onClick={() => onSelectChat(chat.id)}
                  className={cn(
                    "flex w-full items-center gap-3 rounded-[24px] px-4 py-3 text-left transition",
                    isActive ? "bg-primary/10" : "hover:bg-muted/60",
                  )}
                >
                  <Avatar className="h-12 w-12">
                    <AvatarFallback className="bg-primary/10 text-primary">
                      <ChatIcon className="h-4 w-4" />
                    </AvatarFallback>
                  </Avatar>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center justify-between gap-3">
                      <div className="min-w-0">
                        <p className="truncate text-sm font-medium">{label}</p>
                        <p className="mt-0.5 text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
                          {getChatTypeLabel(chat)}
                        </p>
                      </div>
                      <span className="shrink-0 text-[11px] text-muted-foreground">
                        {formatTimestamp(chat.updated_at || chat.created_at)}
                      </span>
                    </div>
                    <p className="mt-1 truncate text-sm text-muted-foreground">
                      {chat.last_message || "No messages yet"}
                    </p>
                  </div>
                </button>
              )
            })
          )}
        </div>
      </ScrollArea>
    </aside>
  )
}

export function ChatConversationPane({
  selectedChat,
  selectedChatId,
  selectedChatLabel,
  participantContacts,
  messages,
  currentUserId,
  messageText,
  onMessageTextChange,
  onComposerKeyDown,
  onSendMessage,
  onBack,
  onOpenDeleteDialog,
  onOpenLeaveDialog,
  onReportChat,
  messagesLoading,
  messagesError,
  isSendPending,
  endRef,
  isMobileConversationOpen,
}: {
  selectedChat: Chat | null
  selectedChatId: string | null
  selectedChatLabel: string
  participantContacts: ChatContact[]
  messages: Message[]
  currentUserId?: string
  messageText: string
  onMessageTextChange: (value: string) => void
  onComposerKeyDown: (event: KeyboardEvent<HTMLTextAreaElement>) => void
  onSendMessage: () => void
  onBack: () => void
  onOpenDeleteDialog: () => void
  onOpenLeaveDialog: () => void
  onReportChat: (chatId: string) => void
  messagesLoading: boolean
  messagesError: unknown
  isSendPending: boolean
  endRef: React.RefObject<HTMLDivElement | null>
  isMobileConversationOpen: boolean
}) {
  const SelectedChatIcon = selectedChat?.chat_type === "group" ? Users : User

  return (
    <section
      className={cn(
        "flex min-w-0 flex-1 flex-col bg-[linear-gradient(180deg,rgba(15,23,42,0.03),transparent_18%,rgba(13,148,136,0.04))]",
        isMobileConversationOpen ? "flex" : "hidden lg:flex",
      )}
    >
      {selectedChat ? (
        <>
          <header className="flex items-center gap-3 border-b border-border/60 bg-background/85 px-4 py-4 backdrop-blur md:px-6">
            <Button
              variant="ghost"
              size="icon"
              className="h-10 w-10 rounded-2xl lg:hidden"
              onClick={onBack}
            >
              <ArrowLeft className="h-4 w-4" />
            </Button>

            <Avatar className="h-11 w-11">
              <AvatarFallback className="bg-primary/10 text-primary">
                <SelectedChatIcon className="h-4 w-4" />
              </AvatarFallback>
            </Avatar>

            <div className="min-w-0 flex-1">
              <h2 className="truncate text-lg font-semibold">{selectedChatLabel}</h2>
              <p className="truncate text-sm text-muted-foreground">
                {getChatTypeLabel(selectedChat)}
                {participantContacts.length > 0
                  ? ` · ${participantContacts.map(getContactLabel).join(", ")}`
                  : ""}
              </p>
            </div>

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="h-10 w-10 rounded-2xl">
                  <MoreHorizontal className="h-5 w-5" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-72 rounded-2xl">
                <DropdownMenuLabel>Participants</DropdownMenuLabel>
                {participantContacts.length > 0 ? (
                  participantContacts.map((contact) => (
                    <DropdownMenuItem key={contact.id} disabled>
                      <Avatar className="h-7 w-7">
                        <AvatarFallback className="text-[10px]">
                          {getInitials(getContactLabel(contact))}
                        </AvatarFallback>
                      </Avatar>
                      <span className="truncate">{getContactLabel(contact)}</span>
                    </DropdownMenuItem>
                  ))
                ) : (
                  <DropdownMenuItem disabled>No other active participants</DropdownMenuItem>
                )}
                <DropdownMenuSeparator />
                <DropdownMenuItem
                  onClick={() => selectedChatId && onReportChat(selectedChatId)}
                >
                  <Flag className="h-4 w-4" />
                  Report chat
                </DropdownMenuItem>
                <DropdownMenuItem variant="destructive" onClick={onOpenLeaveDialog}>
                  <UserRoundMinus className="h-4 w-4" />
                  Leave chat
                </DropdownMenuItem>
                <DropdownMenuItem variant="destructive" onClick={onOpenDeleteDialog}>
                  <Trash2 className="h-4 w-4" />
                  Delete chat
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </header>

          <ScrollArea className="min-h-0 flex-1">
            <div className="mx-auto flex w-full max-w-4xl flex-col gap-4 px-4 py-6 md:px-6">
              {messagesLoading ? (
                Array.from({ length: 5 }).map((_, idx) => (
                  <Skeleton key={idx} className="h-16 w-2/3 rounded-3xl" />
                ))
              ) : messagesError ? (
                <div className="rounded-3xl border border-destructive/20 bg-destructive/5 px-4 py-3 text-sm text-destructive">
                  {messagesError instanceof Error
                    ? messagesError.message
                    : "Failed to load messages"}
                </div>
              ) : messages.length === 0 ? (
                <EmptyState
                  title="No messages yet"
                  description="Send the first message to start this conversation."
                />
              ) : (
                messages.map((message) => {
                  const isOwnMessage = message.sender_id === currentUserId
                  return (
                    <div
                      key={message.id}
                      className={cn(
                        "flex w-full",
                        isOwnMessage ? "justify-end" : "justify-start",
                      )}
                    >
                      <div
                        className={cn(
                          "max-w-[86%] rounded-[24px] px-4 py-3 shadow-[0_12px_30px_-24px_rgba(15,23,42,0.7)] md:max-w-[72%]",
                          isOwnMessage
                            ? "rounded-br-md bg-primary text-primary-foreground"
                            : "rounded-bl-md border border-border/70 bg-background",
                        )}
                      >
                        <p className="whitespace-pre-wrap text-sm leading-6">
                          {message.content}
                        </p>
                        <p
                          className={cn(
                            "mt-2 text-[11px]",
                            isOwnMessage
                              ? "text-primary-foreground/75"
                              : "text-muted-foreground",
                          )}
                        >
                          {formatTimestamp(message.created_at)}
                        </p>
                      </div>
                    </div>
                  )
                })
              )}
              <div ref={endRef} />
            </div>
          </ScrollArea>

          <div className="border-t border-border/60 bg-background/88 px-4 py-4 backdrop-blur md:px-6">
            <div className="mx-auto flex max-w-4xl items-end gap-3">
              <div className="flex-1 rounded-[28px] border border-border/70 bg-background p-2">
                <Textarea
                  value={messageText}
                  onChange={(event) => onMessageTextChange(event.target.value)}
                  onKeyDown={onComposerKeyDown}
                  placeholder="Write a message"
                  className="min-h-14 resize-none border-0 bg-transparent px-3 py-2 shadow-none focus-visible:ring-0"
                />
              </div>
              <Button
                onClick={onSendMessage}
                disabled={!messageText.trim() || isSendPending}
                className="h-14 rounded-[22px] px-5"
              >
                <SendHorizontal className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </>
      ) : (
        <EmptyState
          title="Select a conversation"
          description="Pick a chat from the inbox or start a new one."
        />
      )}
    </section>
  )
}
