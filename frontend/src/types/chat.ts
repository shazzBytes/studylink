// Chat Types - matching backend schemas

export enum ConversationType {
  DIRECT = 1,
  GROUP = 2,
  MENTORSHIP = 3,
  RESEARCH = 4,
}

export enum ConversationStatus {
  ACTIVE = 1,
  ARCHIVED = 2,
  MUTED = 3,
}

export enum MemberStatus {
  ACTIVE = 1,
  LEFT = 2,
  REMOVED = 3,
}

export enum MessageStatus {
  SENT = 1,
  DELIVERED = 2,
  READ = 3,
  DELETED = 4,
}

// Base Types
export interface TimestampBase {
  created_at: string
  updated_at: string
}

export interface IDMixin {
  id: string
}

// Room Types
export interface RoomBase {
  type: ConversationType
  name: string | null
  description: string | null
}

export interface RoomCreate extends RoomBase {}

export interface RoomUpdate {
  name?: string | null
  description?: string | null
  is_archived?: boolean
  status?: ConversationStatus
}

export interface RoomPublic extends RoomBase, IDMixin, TimestampBase {
  created_by: string
  status: ConversationStatus
  is_archived: boolean
  last_message_at: string
  member_count?: number
  unread_count?: number
}

export interface RoomWithMembers extends RoomPublic {
  members: RoomMemberPublic[]
}

export interface RoomsPublic {
  data: RoomPublic[]
  count: number
}

// Room Member Types
export interface RoomMemberBase {
  room_id: string
  user_id: string
}

export interface RoomMemberCreate extends RoomMemberBase {}

export interface RoomMemberUpdate {
  status?: MemberStatus
  is_muted?: boolean
  last_read_at?: string
}

export interface RoomMemberPublic extends RoomMemberBase, IDMixin {
  status: MemberStatus
  joined_at: string
  left_at: string | null
  last_read_at: string | null
  is_muted: boolean
  user_name?: string | null
  user_email?: string | null
}

export interface RoomMembersPublic {
  data: RoomMemberPublic[]
  count: number
}

// Room Admin Types
export interface RoomAdminBase {
  room_id: string
  user_id: string
}

export interface RoomAdminCreate extends RoomAdminBase {}

export interface RoomAdminPublic extends RoomAdminBase, IDMixin {
  assigned_at: string
  assigned_by: string | null
}

// Message Types
export interface MessageBase {
  content: string
}

export interface MessageCreate extends MessageBase {
  room_id: string
  reply_to_id?: string | null
}

export interface MessageUpdate {
  content: string
}

export interface MessagePublic extends MessageBase, IDMixin, TimestampBase {
  room_id: string
  sender_id: string
  status: MessageStatus
  is_edited: boolean
  is_deleted: boolean
  reply_to_id: string | null
  sender_name?: string | null
  reaction_count?: number
  attachment_count?: number
}

export interface MessageWithDetails extends MessagePublic {
  reactions: MessageReactionPublic[]
  attachments: MessageAttachmentPublic[]
  reply_to?: MessagePublic | null
}

export interface MessagesPublic {
  data: MessagePublic[]
  count: number
}

// Message Reaction Types
export interface MessageReactionBase {
  emoji: string
}

export interface MessageReactionCreate extends MessageReactionBase {
  message_id: string
}

export interface MessageReactionPublic extends MessageReactionBase, IDMixin {
  message_id: string
  user_id: string
  created_at: string
}

export interface MessageReactionsPublic {
  data: MessageReactionPublic[]
  count: number
}

// Message Attachment Types
export interface MessageAttachmentBase {
  file_name: string
  file_type: string
  file_size: number
}

export interface MessageAttachmentCreate extends MessageAttachmentBase {
  message_id: string
  file_url: string
}

export interface MessageAttachmentPublic extends MessageAttachmentBase, IDMixin {
  message_id: string
  file_url: string
  created_at: string
}

// WebSocket Types
export interface WSMessageBase {
  type: string
  room_id: string
  timestamp: string
}

export interface WSMessage extends WSMessageBase {
  type: "message"
  sender_id: string
  content: string
  message_id?: string | null
  reply_to_id?: string | null
}

export interface WSTypingIndicator {
  type: "typing"
  room_id: string
  sender_id: string
  is_typing: boolean
}

export interface WSUserStatus extends WSMessageBase {
  user_id: string
}

export interface WSMessageRead extends WSMessageBase {
  type: "read"
  user_id: string
  message_id: string
}

export interface WSMessageReaction extends WSMessageBase {
  type: "reaction"
  message_id: string
  user_id: string
  emoji: string
  action: "add" | "remove"
}

export interface WSError {
  type: "error"
  error: string
  details?: string | null
  timestamp: string
}

export type WSMessageType =
  | WSMessage
  | WSTypingIndicator
  | WSUserStatus
  | WSMessageRead
  | WSMessageReaction
  | WSError
