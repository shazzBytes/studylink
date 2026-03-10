const getApiBase = () => import.meta.env.VITE_API_URL || ""

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
  title: string | null
  participants: string[]
  last_message: string | null
  created_at: string | null
  updated_at: string | null
}

export type ChatsResponse = {
  data: Chat[]
  count: number
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

export const listChats = async (): Promise<ChatsResponse> => {
  const response = await fetch(`${getApiBase()}/api/v1/chats/`, {
    method: "GET",
    headers: getAuthHeaders(),
  })
  return parseResponse<ChatsResponse>(response)
}

export const createChat = async (payload: {
  title?: string
  participants?: string[]
}): Promise<Chat> => {
  const response = await fetch(`${getApiBase()}/api/v1/chats/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({
      title: payload.title || null,
      participants: payload.participants || [],
    }),
  })
  return parseResponse<Chat>(response)
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
