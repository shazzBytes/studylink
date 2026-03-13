import type {
  Chat,
  ChatContact,
  Message,
} from "@/client/chats.api"

export function formatTimestamp(value: string | null) {
  if (!value) return ""

  return new Intl.DateTimeFormat(undefined, {
    hour: "numeric",
    minute: "2-digit",
    month: "short",
    day: "numeric",
  }).format(new Date(value))
}

export function getContactLabel(contact: ChatContact) {
  return contact.full_name?.trim() || contact.email
}

export function getChatLabel(
  chat: Chat | null,
  currentUserId: string | undefined,
  contacts: ChatContact[],
) {
  if (!chat) return "Conversation"
  if (chat.title?.trim()) return chat.title

  const contactMap = new Map(contacts.map((contact) => [contact.id, contact]))
  const others = chat.participants.filter(
    (participantId) => participantId !== currentUserId,
  )
  const labels = others.map((participantId) => {
    const contact = contactMap.get(participantId)
    return contact ? getContactLabel(contact) : "Unknown user"
  })

  if (labels.length === 0) return "Conversation"
  if (labels.length === 1) return labels[0]
  if (labels.length === 2) return `${labels[0]} and ${labels[1]}`
  return `${labels[0]}, ${labels[1]} +${labels.length - 2}`
}

export function getChatTypeLabel(chat: Chat | null) {
  return chat?.chat_type === "group" ? "Group" : "Direct message"
}

export function sortChats(chats: Chat[]) {
  return [...chats].sort((left, right) => {
    const leftTime = left.updated_at || left.created_at || ""
    const rightTime = right.updated_at || right.created_at || ""
    return rightTime.localeCompare(leftTime)
  })
}

export function upsertChat(chats: Chat[], nextChat: Chat) {
  const remainingChats = chats.filter((chat) => chat.id !== nextChat.id)
  return sortChats([nextChat, ...remainingChats])
}

export function appendMessage(messages: Message[], nextMessage: Message) {
  if (messages.some((message) => message.id === nextMessage.id)) return messages
  return [...messages, nextMessage]
}
