#!/usr/bin/env python3
"""
Quick test script for StudyLink Real-Time Messaging
Usage: python3 test_chat.py
"""

import asyncio
import json
import requests
import sys

try:
    import websockets
except ImportError:
    print("❌ Please install websockets: pip install websockets")
    sys.exit(1)

API_BASE = "http://localhost:8000/api/v1"


def login(email: str, password: str) -> str:
    """Login and get access token."""
    print(f"🔐 Logging in as {email}...")
    
    response = requests.post(
        f"{API_BASE}/login/access-token",
        data={"username": email, "password": password}
    )
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        sys.exit(1)
    
    token = response.json()["access_token"]
    print(f"✅ Login successful! Token: {token[:50]}...")
    return token


def get_user_info(token: str) -> dict:
    """Get current user information."""
    response = requests.post(
        f"{API_BASE}/login/test-token",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code != 200:
        print(f"❌ Failed to get user info: {response.text}")
        sys.exit(1)
    
    user = response.json()
    print(f"👤 User ID: {user['id']}")
    return user


def create_room(token: str, user_id: str, room_name: str) -> str:
    """Create a new chat room."""
    print(f"🏠 Creating room: {room_name}...")
    
    response = requests.post(
        f"{API_BASE}/chat/rooms",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "type": 2,  # Group chat
            "name": room_name,
            "created_by": user_id
        }
    )
    
    if response.status_code != 200:
        print(f"❌ Failed to create room: {response.text}")
        sys.exit(1)
    
    room = response.json()
    room_id = room["id"]
    print(f"✅ Room created! ID: {room_id}")
    return room_id


def get_message_history(token: str, room_id: str):
    """Fetch message history."""
    print(f"📜 Fetching message history...")
    
    response = requests.get(
        f"{API_BASE}/chat/rooms/{room_id}/messages?limit=20",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch messages: {response.text}")
        return
    
    result = response.json()
    print(f"📨 Found {result['count']} messages:")
    
    for msg in result['data']:
        timestamp = msg['timestamp'][:19].replace('T', ' ')
        print(f"  [{timestamp}] {msg['sender_id'][:8]}: {msg['content']}")


async def chat_client(token: str, room_id: str, username: str):
    """Connect to WebSocket and chat."""
    uri = f"ws://localhost:8000/api/v1/ws/chat/{room_id}?token={token}"
    
    print(f"\n🚀 Connecting to room {room_id}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected! Type messages (or 'quit' to exit):\n")
            
            # Task to receive messages
            async def receive_messages():
                try:
                    async for message in websocket:
                        data = json.loads(message)
                        
                        if data['type'] == 'message':
                            sender = data.get('sender_email', data.get('sender_id', 'Unknown'))
                            content = data['content']
                            timestamp = data['timestamp'][:19].replace('T', ' ')
                            print(f"\n📨 [{timestamp}] {sender}: {content}")
                            print(f"{username}> ", end='', flush=True)
                        
                        elif data['type'] == 'user_joined':
                            print(f"\n✅ {data['user_email']} joined")
                            print(f"{username}> ", end='', flush=True)
                        
                        elif data['type'] == 'user_left':
                            print(f"\n👋 {data['user_email']} left")
                            print(f"{username}> ", end='', flush=True)
                        
                        elif data['type'] == 'typing':
                            if data['is_typing']:
                                print(f"\n✍️  {data['sender_email']} is typing...")
                                print(f"{username}> ", end='', flush=True)
                
                except websockets.exceptions.ConnectionClosed:
                    print("\n❌ Connection closed")
            
            # Task to send messages
            async def send_messages():
                loop = asyncio.get_event_loop()
                while True:
                    try:
                        # Read from stdin in a non-blocking way
                        message = await loop.run_in_executor(None, input, f"{username}> ")
                        
                        if message.lower() == 'quit':
                            break
                        
                        if message.strip():
                            await websocket.send(json.dumps({
                                "type": "message",
                                "content": message
                            }))
                    except EOFError:
                        break
            
            # Run both tasks concurrently
            receive_task = asyncio.create_task(receive_messages())
            send_task = asyncio.create_task(send_messages())
            
            # Wait for send task to complete (user types 'quit')
            await send_task
            receive_task.cancel()
            
            print("\n👋 Disconnecting...")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")


def main():
    """Main function."""
    print("🚀 StudyLink Real-Time Chat Test (Python)")
    print("=" * 50)
    
    # Get credentials
    email = input("Email (default: admin@example.com): ").strip() or "admin@example.com"
    password = input("Password (default: changethis): ").strip() or "changethis"
    
    # Login
    token = login(email, password)
    user = get_user_info(token)
    
    # Room setup
    print("\n" + "=" * 50)
    choice = input("Create new room or join existing? (new/join, default: new): ").strip() or "new"
    
    if choice.lower() == "new":
        room_name = input("Room name (default: Python Test Room): ").strip() or "Python Test Room"
        room_id = create_room(token, user['id'], room_name)
    else:
        room_id = input("Enter room ID: ").strip()
    
    # Fetch message history
    print("\n" + "=" * 50)
    get_message_history(token, room_id)
    
    # Start chat
    print("\n" + "=" * 50)
    print("Instructions:")
    print("  - Type a message and press Enter to send")
    print("  - Type 'quit' to exit")
    print("  - Open the HTML client in a browser to test real-time updates")
    print("=" * 50)
    
    username = user['email'].split('@')[0]
    
    try:
        asyncio.run(chat_client(token, room_id, username))
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")


if __name__ == "__main__":
    main()
