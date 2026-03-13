const getApiBase = () => import.meta.env.VITE_API_URL || ""
const getSocketBase = () => {
  const apiBase = getApiBase() || window.location.origin
  if (apiBase.startsWith("https://")) return `wss://${apiBase.slice(8)}`
  if (apiBase.startsWith("http://")) return `ws://${apiBase.slice(7)}`
  return apiBase
}

const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token")
  return {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "",
  }
}

const parseResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    let detail = "Request failed"
    try {
      const body = await response.json()
      detail = body?.detail || detail
    } catch {
      // Ignore JSON parse errors for non-JSON responses.
    }
    throw new Error(detail)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return (await response.json()) as T
}

export type Chat = {
  id: string
  user_id: string
  chat_type: "dm" | "group"
  title: string | null
  participants: string[]
  reported_by: string[]
  last_message: string | null
  created_at: string | null
  updated_at: string | null
}

export type ChatsResponse = {
  data: Chat[]
  count: number
}

export type ChatContact = {
  id: string
  email: string
  full_name: string | null
}

export type Message = {
  id: string
  chat_id: string
  sender_id: string
  content: string
  attachments: string[]
  created_at: string | null
  updated_at: string | null
  is_deleted: boolean
}

export type MessagesResponse = {
  data: Message[]
  count: number
}

export type ChatSocketEvent =
  | { type: "chat.created"; chat: Chat }
  | { type: "chat.updated"; chat: Chat }
  | { type: "chat.deleted"; chat_id: string }
  | { type: "chat.left"; chat_id: string }
  | { type: "message.created"; chat: Chat; message: Message }

export const listChats = async (): Promise<ChatsResponse> => {
  const response = await fetch(`${getApiBase()}/api/v1/chats/`, {
    method: "GET",
    headers: getAuthHeaders(),
  })
  return parseResponse<ChatsResponse>(response)
}

export const createChat = async (payload: {
  title?: string | null
  participants: string[]
}): Promise<Chat> => {
  const response = await fetch(`${getApiBase()}/api/v1/chats/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({
      title: payload.title || null,
      participants: payload.participants,
    }),
  })
  return parseResponse<Chat>(response)
}

export const listChatContacts = async (q?: string): Promise<ChatContact[]> => {
  const searchParams = new URLSearchParams()
  if (q?.trim()) searchParams.set("q", q.trim())
  searchParams.set("limit", "20")

  const response = await fetch(
    `${getApiBase()}/api/v1/chats/contacts?${searchParams.toString()}`,
    {
      method: "GET",
      headers: getAuthHeaders(),
    },
  )
  return parseResponse<ChatContact[]>(response)
}

export const listMessages = async (chatId: string): Promise<MessagesResponse> => {
  const response = await fetch(`${getApiBase()}/api/v1/chats/${chatId}/messages/`, {
    method: "GET",
    headers: getAuthHeaders(),
  })
  return parseResponse<MessagesResponse>(response)
}

export const createMessage = async (
  chatId: string,
  payload: { content: string; attachments?: string[] },
): Promise<Message> => {
  const response = await fetch(`${getApiBase()}/api/v1/chats/${chatId}/messages/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({
      content: payload.content,
      attachments: payload.attachments || [],
    }),
  })
  return parseResponse<Message>(response)
}

export const deleteChat = async (
  chatId: string,
): Promise<{ message: string }> => {
  const response = await fetch(`${getApiBase()}/api/v1/chats/${chatId}/`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  })
  return parseResponse<{ message: string }>(response)
}

export const leaveChat = async (
  chatId: string,
): Promise<{ message: string }> => {
  const response = await fetch(`${getApiBase()}/api/v1/chats/${chatId}/leave`, {
    method: "POST",
    headers: getAuthHeaders(),
  })
  return parseResponse<{ message: string }>(response)
}

export const reportChat = async (
  chatId: string,
): Promise<{ message: string }> => {
  const response = await fetch(`${getApiBase()}/api/v1/chats/${chatId}/report`, {
    method: "POST",
    headers: getAuthHeaders(),
  })
  return parseResponse<{ message: string }>(response)
}

export const createChatsWebSocket = (): WebSocket | null => {
  const token = localStorage.getItem("access_token")
  if (!token) return null

  return new WebSocket(
    `${getSocketBase()}/api/v1/chats/ws?token=${encodeURIComponent(token)}`,
  )
}
