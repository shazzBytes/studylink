# Chat Service Frontend Documentation

## Overview

A comprehensive real-time messaging frontend built with React, TypeScript, TanStack Router, and TanStack Query. Features include real-time messaging, room management, message reactions, typing indicators, and WebSocket support.

## Features

- ✅ **Real-time Messaging** - WebSocket-based instant messaging
- ✅ **Room Management** - Create, update, and archive chat rooms
- ✅ **Multiple Room Types** - Direct, Group, Mentorship, and Research rooms
- ✅ **Message Operations** - Send, edit, delete, and reply to messages
- ✅ **Reactions** - Add emoji reactions to messages
- ✅ **Typing Indicators** - Real-time typing status
- ✅ **Read Receipts** - Message delivery and read status
- ✅ **Member Management** - Admin-controlled member operations
- ✅ **Responsive Design** - Mobile and desktop optimized
- ✅ **DRY Architecture** - Reusable hooks, components, and types

## Project Structure

```
frontend/src/
├── types/
│   └── chat.ts                 # TypeScript types and interfaces
├── hooks/
│   ├── useChat.ts              # Chat API hooks (queries/mutations)
│   └── useWebSocket.ts         # WebSocket connection management
├── components/
│   └── Chat/
│       ├── ChatList.tsx        # Room list sidebar
│       ├── ChatRoomCard.tsx    # Individual room card
│       ├── ChatRoom.tsx        # Main chat interface
│       ├── MessageBubble.tsx   # Message display component
│       ├── MessageInput.tsx    # Message composition
│       └── CreateRoomDialog.tsx # Room creation dialog
└── routes/
    └── _layout/
        └── messages.tsx        # Messages page route
```

## Types System

### Room Types
- `RoomCreate` - Create new room
- `RoomUpdate` - Update room details
- `RoomPublic` - Public room data
- `RoomWithMembers` - Room with member list

### Message Types
- `MessageCreate` - Send new message
- `MessageUpdate` - Edit message
- `MessagePublic` - Message data
- `MessageWithDetails` - Message with reactions/attachments

### WebSocket Types
- `WSMessage` - Chat message event
- `WSTypingIndicator` - Typing status
- `WSUserStatus` - User joined/left
- `WSMessageRead` - Read receipt
- `WSMessageReaction` - Reaction event
- `WSError` - Error event

## Hooks

### useChat.ts

Core chat operations using TanStack Query:

```typescript
// Queries
const { data: rooms } = useRooms()
const { data: room } = useRoom(roomId)
const { data: messages } = useMessages(roomId)

// Mutations
const createRoom = useCreateRoom()
const sendMessage = useSendMessage()
const updateMessage = useUpdateMessage()
const deleteMessage = useDeleteMessage()
const addReaction = useAddReaction()
const leaveRoom = useLeaveRoom()
```

### useWebSocket.ts

WebSocket connection management:

```typescript
const { isConnected, sendMessage, disconnect, reconnect } = useWebSocket(
  wsUrl,
  {
    onMessage: (data) => console.log(data),
    onConnect: () => console.log('Connected'),
    onDisconnect: () => console.log('Disconnected'),
    reconnectInterval: 3000,
    maxReconnectAttempts: 5,
  }
)
```

## Components

### ChatList

Room list sidebar with search and filtering:

```tsx
<ChatList
  activeRoomId={selectedRoom?.id}
  onRoomSelect={(room) => setSelectedRoom(room)}
  onCreateRoom={() => setIsCreateRoomOpen(true)}
/>
```

### ChatRoom

Main chat interface with messages and input:

```tsx
<ChatRoom
  room={selectedRoom}
  onViewMembers={() => {}}
  onRoomSettings={() => {}}
/>
```

### MessageBubble

Individual message display:

```tsx
<MessageBubble
  message={message}
  isOwn={message.sender_id === user?.id}
  onEdit={() => {}}
  onDelete={() => {}}
  onReact={(emoji) => {}}
  onReply={() => {}}
/>
```

### MessageInput

Message composition with reply support:

```tsx
<MessageInput
  onSend={(content) => {}}
  onTyping={(isTyping) => {}}
  replyTo={replyTo}
  onCancelReply={() => {}}
/>
```

### CreateRoomDialog

Room creation modal:

```tsx
<CreateRoomDialog
  open={isOpen}
  onOpenChange={setIsOpen}
/>
```

## API Integration

### TODO: Update Client API

The `useChat.ts` hook currently uses placeholder API functions. You need to implement actual API calls in your client:

```typescript
// Example: Add to your API client (e.g., src/client/sdk.gen.ts)
export class ChatService {
  static async getRooms(skip = 0, limit = 100): Promise<RoomsPublic> {
    return request({
      method: 'GET',
      url: '/api/v1/chat/rooms',
      params: { skip, limit },
    })
  }

  static async sendMessage(data: MessageCreate): Promise<MessagePublic> {
    return request({
      method: 'POST',
      url: '/api/v1/chat/messages',
      body: data,
    })
  }

  // ... more methods
}
```

Then update `useChat.ts` to use your client:

```typescript
import { ChatService } from '@/client'

const ChatAPI = {
  getRooms: ChatService.getRooms,
  sendMessage: ChatService.sendMessage,
  // ... etc
}
```

## WebSocket Configuration

Set up WebSocket connection in your chat page:

```typescript
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws'

const { sendMessage: sendWsMessage } = useWebSocket(
  `${WS_URL}/chat/${roomId}?token=${accessToken}`,
  {
    onMessage: (data) => {
      // Handle incoming WebSocket messages
      switch (data.type) {
        case 'message':
          // Invalidate messages query to fetch new message
          queryClient.invalidateQueries(['chat', 'messages', roomId])
          break
        case 'typing':
          // Update typing indicator state
          break
        case 'reaction':
          // Update message reactions
          break
      }
    },
  }
)
```

## Environment Variables

Add to your `.env` file:

```env
VITE_WS_URL=ws://localhost:8000/ws
```

## Styling

The components use Tailwind CSS with shadcn/ui components. All styling is consistent with your existing design system.

### Custom Styles
- Message bubbles adapt to light/dark mode
- Active states for selected rooms
- Smooth transitions and animations
- Responsive layout for mobile/desktop

## Permissions

Admin-only operations are handled in the backend CRUD. The frontend respects these permissions by:

1. Showing/hiding admin actions based on user role
2. Handling 403 errors gracefully
3. Displaying appropriate error messages

## Next Steps

1. **Implement Backend Routes** - Create FastAPI endpoints for chat operations
2. **Connect WebSocket** - Set up WebSocket endpoint in backend
3. **Generate API Client** - Run `npm run generate-client` to update types
4. **Add File Uploads** - Implement attachment upload functionality
5. **Add Notifications** - Integrate with notification system
6. **Add Voice/Video** - Add WebRTC for calls (optional)

## Testing

Test the frontend with mock data:

```typescript
// Add to your test file
const mockRoom: RoomPublic = {
  id: '123',
  type: ConversationType.GROUP,
  name: 'Test Room',
  description: 'Test description',
  created_by: 'user-1',
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  status: ConversationStatus.ACTIVE,
  is_archived: false,
  last_message_at: new Date().toISOString(),
}
```

## Dependencies

Required packages (already in package.json):
- `@tanstack/react-query` - Data fetching and caching
- `@tanstack/react-router` - Routing
- `date-fns` - Date formatting
- `lucide-react` - Icons
- Radix UI components (via shadcn/ui)

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- WebSocket support required
- Responsive design for mobile and tablet

## Performance Optimizations

- Query caching with TanStack Query
- Optimistic updates for instant feedback
- Virtual scrolling for long message lists (TODO)
- Lazy loading of older messages
- WebSocket reconnection with exponential backoff

## Known Limitations

1. File attachments UI is present but upload logic needs implementation
2. Voice/Video call buttons are disabled (placeholder)
3. Search functionality needs backend support
4. Message notifications need integration with notification system

## License

Same as parent project
