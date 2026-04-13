import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import type {
  MessageCreate,
  MessagePublic,
  MessageUpdate,
  MessagesPublic,
  RoomCreate,
  RoomMemberCreate,
  RoomPublic,
  RoomsPublic,
  RoomUpdate,
  MessageReactionCreate,
} from "@/types/chat"
import { handleError } from "@/utils"
import useCustomToast from "./useCustomToast"
import axios from "axios"

const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api/v1"

function authHeaders() {
  const token = localStorage.getItem("access_token")
  return token ? { Authorization: `Bearer ${token}` } : {}
}

const ChatAPI = {
  getRooms: async (skip = 0, limit = 100): Promise<RoomsPublic> => {
    const res = await axios.get(`${API_BASE}/chat/rooms`, {
      params: { skip, limit },
      headers: authHeaders(),
    })
    // backend may return a plain list of rooms (list[RoomPublic]) or a paginated object
    if (Array.isArray(res.data)) {
      return { data: res.data as any[], count: (res.data as any[]).length }
    }
    return res.data as RoomsPublic
  },
  getRoom: async (roomId: string): Promise<RoomPublic> => {
    const res = await axios.get(`${API_BASE}/chat/rooms/${roomId}`, {
      headers: authHeaders(),
    })
    return res.data as RoomPublic
  },
  createRoom: async (data: RoomCreate): Promise<RoomPublic> => {
    const res = await axios.post(`${API_BASE}/chat/rooms`, data, {
      headers: { ...authHeaders(), "Content-Type": "application/json" },
    })
    return res.data as RoomPublic
  },
  // backend currently doesn't provide update room endpoint; emulate with get
  updateRoom: async (roomId: string, data: RoomUpdate): Promise<RoomPublic> => {
    const res = await axios.get(`${API_BASE}/chat/rooms/${roomId}`, {
      headers: authHeaders(),
    })
    return res.data as RoomPublic
  },
  deleteRoom: async (roomId: string): Promise<void> => {
    // backend has no delete room endpoint; no-op
    return Promise.resolve()
  },

  addMember: async (data: RoomMemberCreate): Promise<void> => {
    await axios.post(`${API_BASE}/chat/rooms/${data.room_id}/members`, null, {
      params: { user_id: data.user_id },
      headers: authHeaders(),
    })
  },
  removeMember: async (roomId: string, userId: string): Promise<void> => {
    await axios.delete(`${API_BASE}/chat/rooms/${roomId}/members`, {
      params: { user_id: userId },
      headers: authHeaders(),
    })
  },
  leaveRoom: async (roomId: string): Promise<void> => {
    await axios.post(`${API_BASE}/chat/rooms/${roomId}/leave`, null, { headers: authHeaders() }).catch(() => {})
  },

  getMessages: async (roomId: string, skip = 0, limit = 50): Promise<MessagesPublic> => {
    const res = await axios.get(`${API_BASE}/chat/rooms/${roomId}/messages`, {
      params: { skip, limit },
      headers: authHeaders(),
    })
    return res.data as MessagesPublic
  },
  sendMessage: async (data: MessageCreate): Promise<MessagePublic> => {
    const res = await axios.post(`${API_BASE}/chat/rooms/${data.room_id}/messages`, { content: data.content }, {
      headers: { ...authHeaders(), "Content-Type": "application/json" },
    })
    return res.data as MessagePublic
  },
  updateMessage: async (messageId: string, data: MessageUpdate): Promise<MessagePublic> => {
    const res = await axios.put(`${API_BASE}/chat/messages/${messageId}`, data, { headers: authHeaders() })
    return res.data as MessagePublic
  },
  deleteMessage: async (messageId: string): Promise<void> => {
    await axios.delete(`${API_BASE}/chat/messages/${messageId}`, { headers: authHeaders() })
  },

  addReaction: async (data: MessageReactionCreate): Promise<void> => {
    await axios.post(`${API_BASE}/chat/messages/${data.message_id}/reactions`, { emoji: data.emoji }, { headers: { ...authHeaders(), "Content-Type": "application/json" } })
  },
  removeReaction: async (messageId: string, emoji: string): Promise<void> => {
    await axios.delete(`${API_BASE}/chat/messages/${messageId}/reactions`, { params: { emoji }, headers: authHeaders() })
  },
}

// Query keys
export const chatKeys = {
  all: ["chat"] as const,
  rooms: () => [...chatKeys.all, "rooms"] as const,
  room: (roomId: string) => [...chatKeys.rooms(), roomId] as const,
  messages: (roomId: string) => [...chatKeys.room(roomId), "messages"] as const,
}

// Hook: Get all rooms
export const useRooms = (skip = 0, limit = 100) => {
  return useQuery({
    queryKey: [...chatKeys.rooms(), skip, limit],
    queryFn: () => ChatAPI.getRooms(skip, limit),
  })
}

// Hook: Get single room
export const useRoom = (roomId: string | null) => {
  return useQuery({
    queryKey: chatKeys.room(roomId || ""),
    queryFn: () => ChatAPI.getRoom(roomId!),
    enabled: !!roomId,
  })
}

// Hook: Get messages for a room
export const useMessages = (roomId: string | null, skip = 0, limit = 50) => {
  return useQuery({
    queryKey: [...chatKeys.messages(roomId || ""), skip, limit],
    queryFn: () => ChatAPI.getMessages(roomId!, skip, limit),
    enabled: !!roomId,
  })
}

// Hook: Create room
export const useCreateRoom = () => {
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()

  return useMutation({
    mutationFn: (data: RoomCreate) => ChatAPI.createRoom(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.rooms() })
      showSuccessToast("Room created successfully")
    },
    onError: (error) => handleError(error, showErrorToast),
  })
}

// Hook: Update room
export const useUpdateRoom = () => {
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()

  return useMutation({
    mutationFn: ({ roomId, data }: { roomId: string; data: RoomUpdate }) =>
      ChatAPI.updateRoom(roomId, data),
    onSuccess: (_, { roomId }) => {
      queryClient.invalidateQueries({ queryKey: chatKeys.room(roomId) })
      queryClient.invalidateQueries({ queryKey: chatKeys.rooms() })
      showSuccessToast("Room updated successfully")
    },
    onError: (error) => handleError(error, showErrorToast),
  })
}

// Hook: Delete room
export const useDeleteRoom = () => {
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()

  return useMutation({
    mutationFn: (roomId: string) => ChatAPI.deleteRoom(roomId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.rooms() })
      showSuccessToast("Room deleted successfully")
    },
    onError: (error) => handleError(error, showErrorToast),
  })
}

// Hook: Send message
export const useSendMessage = () => {
  const queryClient = useQueryClient()
  const { showErrorToast } = useCustomToast()

  return useMutation({
    mutationFn: (data: MessageCreate) => ChatAPI.sendMessage(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: chatKeys.messages(variables.room_id),
      })
      queryClient.invalidateQueries({
        queryKey: chatKeys.room(variables.room_id),
      })
    },
    onError: (error) => handleError(error, showErrorToast),
  })
}

// Hook: Update message
export const useUpdateMessage = () => {
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()

  return useMutation({
    mutationFn: ({
      messageId,
      data,
      roomId,
    }: {
      messageId: string
      data: MessageUpdate
      roomId: string
    }) => ChatAPI.updateMessage(messageId, data),
    onSuccess: (_, { roomId }) => {
      queryClient.invalidateQueries({ queryKey: chatKeys.messages(roomId) })
      showSuccessToast("Message updated")
    },
    onError: (error) => handleError(error, showErrorToast),
  })
}

// Hook: Delete message
export const useDeleteMessage = () => {
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()

  return useMutation({
    mutationFn: ({ messageId, roomId }: { messageId: string; roomId: string }) =>
      ChatAPI.deleteMessage(messageId),
    onSuccess: (_, { roomId }) => {
      queryClient.invalidateQueries({ queryKey: chatKeys.messages(roomId) })
      showSuccessToast("Message deleted")
    },
    onError: (error) => handleError(error, showErrorToast),
  })
}

// Hook: Add reaction
export const useAddReaction = () => {
  const queryClient = useQueryClient()
  const { showErrorToast } = useCustomToast()

  return useMutation({
    mutationFn: ({
      data,
      roomId,
    }: {
      data: MessageReactionCreate
      roomId: string
    }) => ChatAPI.addReaction(data),
    onSuccess: (_, { roomId }) => {
      queryClient.invalidateQueries({ queryKey: chatKeys.messages(roomId) })
    },
    onError: (error) => handleError(error, showErrorToast),
  })
}

// Hook: Remove reaction
export const useRemoveReaction = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({
      messageId,
      emoji,
      roomId,
    }: {
      messageId: string
      emoji: string
      roomId: string
    }) => ChatAPI.removeReaction(messageId, emoji),
    onSuccess: (_, { roomId }) => {
      queryClient.invalidateQueries({ queryKey: chatKeys.messages(roomId) })
    },
  })
}

// Hook: Leave room
export const useLeaveRoom = () => {
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()

  return useMutation({
    mutationFn: (roomId: string) => ChatAPI.leaveRoom(roomId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.rooms() })
      showSuccessToast("You left the room")
    },
    onError: (error) => handleError(error, showErrorToast),
  })
}
