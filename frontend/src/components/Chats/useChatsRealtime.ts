import { useEffect, useRef } from "react"
import type { QueryClient } from "@tanstack/react-query"

import {
  createChatsWebSocket,
  type Chat,
  type ChatSocketEvent,
  type ChatsResponse,
  type Message,
  type MessagesResponse,
} from "@/client/chats.api"
import { appendMessage, upsertChat } from "@/components/Chats/chats-utils"

type UseChatsRealtimeParams = {
  currentUserId?: string
  queryClient: QueryClient
  onChatRemoved: (chatId: string) => void
}

export function useChatsRealtime({
  currentUserId,
  queryClient,
  onChatRemoved,
}: UseChatsRealtimeParams) {
  const websocketRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<number | null>(null)

  useEffect(() => {
    if (!currentUserId) return

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
      onChatRemoved(chatId)
    }

    const syncMessageInCache = (chatId: string, message: Message) => {
      queryClient.setQueryData<MessagesResponse>(["messages", chatId], (current) => ({
        data: appendMessage(current?.data ?? [], message),
        count: current?.data.some((currentMessage) => currentMessage.id === message.id)
          ? current.count
          : (current?.count ?? 0) + 1,
      }))
    }

    let disposed = false

    const connect = () => {
      const socket = createChatsWebSocket()
      if (!socket) return

      websocketRef.current = socket

      socket.onmessage = (event) => {
        let socketEvent: ChatSocketEvent
        try {
          socketEvent = JSON.parse(event.data) as ChatSocketEvent
        } catch {
          return
        }

        switch (socketEvent.type) {
          case "chat.created":
          case "chat.updated":
            syncChatInCache(socketEvent.chat)
            break
          case "chat.deleted":
          case "chat.left":
            removeChatFromCache(socketEvent.chat_id)
            break
          case "message.created":
            syncChatInCache(socketEvent.chat)
            syncMessageInCache(socketEvent.chat.id, socketEvent.message)
            break
        }
      }

      socket.onerror = () => {
        socket.close()
      }

      socket.onclose = () => {
        if (disposed) return
        reconnectTimeoutRef.current = window.setTimeout(connect, 1500)
      }
    }

    connect()

    return () => {
      disposed = true
      if (reconnectTimeoutRef.current) {
        window.clearTimeout(reconnectTimeoutRef.current)
      }
      websocketRef.current?.close()
      websocketRef.current = null
    }
  }, [currentUserId, onChatRemoved, queryClient])
}
