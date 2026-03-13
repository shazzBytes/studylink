# Real-Time Messaging Service

A complete WebSocket-based real-time messaging system for StudyLink.

## Features

✅ **Real-time messaging** via WebSockets  
✅ **Typing indicators** to show when users are typing  
✅ **Online presence** tracking for room members  
✅ **Message persistence** with PostgreSQL  
✅ **JWT authentication** for secure WebSocket connections  
✅ **Room-based chat** (DM, Group, Mentorship, Research)  
✅ **Message history** with pagination  
✅ **RESTful endpoints** for HTTP-based operations  

## Architecture

### Components

1. **WebSocket Manager** ([core/websocket_manager.py](backend/app/core/websocket_manager.py))
   - Manages active WebSocket connections
   - Handles room-based message broadcasting
   - Tracks online users per room

2. **WebSocket Routes** ([api/routes/websocket.py](backend/app/api/routes/websocket.py))
   - WebSocket endpoint: `/api/v1/ws/chat/{room_id}`
   - Handles real-time message events
   - Supports typing indicators and presence

3. **REST API Routes** ([api/routes/messages.py](backend/app/api/routes/messages.py))
   - Create/manage rooms
   - Fetch message history
   - Send messages via HTTP (fallback)

4. **Models** ([models/chats.py](backend/app/models/chats.py))
   - `Room`: Chat rooms/conversations
   - `Message`: Individual messages
   - `RoomMembers`: Room membership

## API Endpoints

### REST Endpoints

```
POST   /api/v1/chat/rooms                    # Create a new room
GET    /api/v1/chat/rooms                    # Get my rooms
GET    /api/v1/chat/rooms/{room_id}          # Get room details
POST   /api/v1/chat/rooms/{room_id}/members  # Add member to room
GET    /api/v1/chat/rooms/{room_id}/messages # Get message history
POST   /api/v1/chat/rooms/{room_id}/messages # Send message (HTTP)
DELETE /api/v1/messages/{message_id}         # Delete message
GET    /api/v1/rooms/{room_id}/online-users  # Get online user count
```

### WebSocket Endpoint

```
WS /api/v1/ws/chat/{room_id}?token={jwt_token}
```

## Usage

### 1. Create a Room (REST)

```bash
curl -X POST "http://localhost:8000/api/v1/chat/rooms" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": 1,
    "name": "General Discussion",
    "created_by": "user-uuid"
  }'
```

### 2. Connect to WebSocket

#### JavaScript Client

```javascript
const token = "YOUR_JWT_TOKEN";
const roomId = "room-uuid";
const ws = new WebSocket(`ws://localhost:8000/api/v1/ws/chat/${roomId}?token=${token}`);

ws.onopen = () => {
  console.log("Connected to chat");
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("Message:", data);
  
  switch(data.type) {
    case 'message':
      displayMessage(data.content, data.sender_email);
      break;
    case 'typing':
      showTypingIndicator(data.sender_email, data.is_typing);
      break;
    case 'user_joined':
      console.log(`${data.user_email} joined`);
      break;
    case 'user_left':
      console.log(`${data.user_email} left`);
      break;
  }
};

// Send a message
function sendMessage(content) {
  ws.send(JSON.stringify({
    type: "message",
    content: content
  }));
}

// Send typing indicator
function sendTyping(isTyping) {
  ws.send(JSON.stringify({
    type: "typing",
    is_typing: isTyping
  }));
}
```

#### Python Client

```python
import asyncio
import websockets
import json

async def chat_client(token: str, room_id: str):
    uri = f"ws://localhost:8000/api/v1/ws/chat/{room_id}?token={token}"
    
    async with websockets.connect(uri) as websocket:
        # Send a message
        await websocket.send(json.dumps({
            "type": "message",
            "content": "Hello from Python!"
        }))
        
        # Receive messages
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {data}")

# Run the client
asyncio.run(chat_client("YOUR_JWT_TOKEN", "room-uuid"))
```

### 3. Fetch Message History (REST)

```bash
curl "http://localhost:8000/api/v1/chat/rooms/{room_id}/messages?skip=0&limit=50" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Message Types

### 1. Chat Message
```json
{
  "type": "message",
  "content": "Hello, world!"
}
```

Server broadcasts:
```json
{
  "type": "message",
  "message_id": "uuid",
  "room_id": "uuid",
  "sender_id": "uuid",
  "sender_email": "user@example.com",
  "content": "Hello, world!",
  "timestamp": "2026-01-03T12:34:56.789Z"
}
```

### 2. Typing Indicator
```json
{
  "type": "typing",
  "is_typing": true
}
```

Server broadcasts to others:
```json
{
  "type": "typing",
  "room_id": "uuid",
  "sender_id": "uuid",
  "sender_email": "user@example.com",
  "is_typing": true
}
```

### 3. System Events

**User Joined:**
```json
{
  "type": "user_joined",
  "room_id": "uuid",
  "user_id": "uuid",
  "user_email": "user@example.com"
}
```

**User Left:**
```json
{
  "type": "user_left",
  "room_id": "uuid",
  "user_id": "uuid",
  "user_email": "user@example.com"
}
```

## Room Types

```python
class ConversationType(IntEnum):
    DIRECT = 1      # One-on-one chat
    GROUP = 2       # Group chat
    MENTORSHIP = 3  # Mentorship conversations
    RESEARCH = 4    # Research project discussions
```

## Testing

### Using the Test HTML Client

1. Open [test_websocket.html](backend/test_websocket.html) in a browser
2. Get your JWT token from login endpoint
3. Enter room ID and token
4. Click "Connect"
5. Start chatting!

### Manual Testing

```bash
# 1. Login to get JWT token
curl -X POST "http://localhost:8000/api/v1/login/access-token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password"

# 2. Create a room
curl -X POST "http://localhost:8000/api/v1/chat/rooms" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type": 1, "name": "Test Room", "created_by": "user-uuid"}'

# 3. Connect via WebSocket using the test HTML client
# or use wscat:
npm install -g wscat
wscat -c "ws://localhost:8000/api/v1/ws/chat/{room_id}?token=$TOKEN"
```

## Security

- ✅ JWT authentication required for WebSocket connections
- ✅ Room membership verification before allowing connections
- ✅ Message sender verification for deletions
- ✅ Automatic cleanup of disconnected clients
- ✅ Token passed via query parameter (WebSocket limitation)

## Performance Considerations

1. **Connection Pooling**: WebSocket connections are lightweight
2. **Message Broadcasting**: Only sends to room members
3. **Automatic Cleanup**: Removes disconnected clients
4. **Pagination**: Message history uses pagination to reduce load
5. **Database Indexing**: Ensure indexes on:
   - `message.room_id`
   - `message.timestamp`
   - `roommembers.room_id`
   - `roommembers.sender_id`

## Frontend Integration Example (React)

```typescript
import { useEffect, useState, useRef } from 'react';

interface Message {
  id: string;
  sender_email: string;
  content: string;
  timestamp: string;
}

export function useChat(roomId: string, token: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(
      `ws://localhost:8000/api/v1/ws/chat/${roomId}?token=${token}`
    );

    ws.onopen = () => {
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'message') {
        setMessages(prev => [...prev, {
          id: data.message_id,
          sender_email: data.sender_email,
          content: data.content,
          timestamp: data.timestamp
        }]);
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
    };

    wsRef.current = ws;

    return () => {
      ws.close();
    };
  }, [roomId, token]);

  const sendMessage = (content: string) => {
    if (wsRef.current && isConnected) {
      wsRef.current.send(JSON.stringify({
        type: 'message',
        content
      }));
    }
  };

  const sendTyping = (isTyping: boolean) => {
    if (wsRef.current && isConnected) {
      wsRef.current.send(JSON.stringify({
        type: 'typing',
        is_typing: isTyping
      }));
    }
  };

  return { messages, isConnected, sendMessage, sendTyping };
}
```

## Future Enhancements

- [ ] Read receipts (mark messages as read)
- [ ] Message reactions (emoji reactions)
- [ ] File/image sharing
- [ ] Voice/video calls
- [ ] Message editing
- [ ] Message threading/replies
- [ ] User presence (online/offline/away)
- [ ] Push notifications for offline users
- [ ] Message search
- [ ] Encryption for sensitive messages

## Troubleshooting

### WebSocket Connection Fails

1. Check JWT token is valid and not expired
2. Verify user is a member of the room
3. Ensure WebSocket URL uses `ws://` (or `wss://` for HTTPS)
4. Check CORS settings in FastAPI

### Messages Not Appearing

1. Verify room_id is correct
2. Check user has membership in room
3. Look at browser console for errors
4. Check backend logs for WebSocket errors

### High Latency

1. Check network conditions
2. Consider using Redis for scaling across multiple servers
3. Implement message queuing for high-traffic scenarios

## Database Migrations

If you need to update the database schema:

```bash
cd backend
alembic revision --autogenerate -m "Add chat tables"
alembic upgrade head
```

---

**Note**: This implementation uses in-memory connection management. For production with multiple server instances, consider using Redis Pub/Sub or a similar distributed message broker.
