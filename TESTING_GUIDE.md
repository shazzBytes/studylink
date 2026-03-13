# Real-Time Messaging Testing Guide

## Quick Start

You have **3 easy ways** to test the real-time messaging:

---

## Method 1: 🌐 HTML Test Client (Recommended for Beginners)

**Easiest way with a visual interface!**

1. **Start your backend:**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Open the test client:**
   - Open `backend/test_websocket.html` in your web browser
   - Or visit: `file:///path/to/studylink/backend/test_websocket.html`

3. **Follow the 3-step wizard:**
   - **Step 1:** Login with your credentials (defaults shown)
   - **Step 2:** Create a new room or enter existing room ID
   - **Step 3:** Start chatting!

4. **Test with multiple users:**
   - Open the same HTML file in multiple browser tabs
   - Each tab can login as a different user
   - Chat in real-time between tabs!

---

## Method 2: 🐍 Python Script (For Developers)

**Interactive command-line chat client!**

1. **Install websockets:**
   ```bash
   pip install websockets requests
   ```

2. **Run the test script:**
   ```bash
   cd backend
   python3 test_chat.py
   ```

3. **Follow the prompts:**
   - Enter email (default: admin@example.com)
   - Enter password (default: changethis)
   - Choose to create new room or join existing
   - Start typing messages!

4. **Type 'quit' to exit**

---

## Method 3: 🔧 Bash Script (Quick Setup)

**Get credentials and test with any WebSocket client!**

1. **Run the setup script:**
   ```bash
   cd backend
   ./test_websocket.sh
   ```

2. **The script will:**
   - Login and get your JWT token
   - Create a room (or use existing)
   - Display all credentials needed
   - Show instructions for various testing tools

3. **Then test with:**
   - The HTML client (method 1)
   - wscat: `wscat -c "ws://localhost:8000/api/v1/ws/chat/{ROOM_ID}?token={TOKEN}"`
   - Or any WebSocket tool

---

## Default Credentials

Check your `.env` file for:
- **Email:** Value of `FIRST_SUPERUSER` (e.g., admin@example.com)
- **Password:** Value of `FIRST_SUPERUSER_PASSWORD` (e.g., changethis)

If you don't have users yet:
```bash
cd backend
python -m app.initial_data
```

---

## Testing Scenarios

### Scenario 1: Two Users Chatting

1. Open `test_websocket.html` in Chrome
2. Login as user1 and create a room
3. Copy the Room ID
4. Open `test_websocket.html` in Firefox (or new Chrome window)
5. Login as user2 and join the same room
6. Start chatting!

### Scenario 2: Python + HTML

1. Run `python3 test_chat.py` in terminal
2. Open `test_websocket.html` in browser
3. Join the same room in both
4. See messages appear in real-time!

### Scenario 3: Multiple Tabs

1. Open multiple tabs with `test_websocket.html`
2. Login as same or different users
3. Join the same room
4. Test typing indicators and presence

---

## What to Test

- ✅ **Messages** - Send and receive in real-time
- ✅ **Typing Indicators** - Type in one window, see in another
- ✅ **User Presence** - See when users join/leave
- ✅ **Message History** - Load previous messages
- ✅ **Reconnection** - Disconnect and reconnect
- ✅ **Multiple Rooms** - Create and switch between rooms

---

## Troubleshooting

### "Login failed"
- Check your credentials in `.env`
- Make sure backend is running: `uvicorn app.main:app --reload`
- Verify database is running: `docker-compose up -d db`

### "Connection failed"
- Ensure backend is running on port 8000
- Check WebSocket URL uses `ws://` (not `wss://` for local)
- Look at browser console for detailed errors

### "Invalid token"
- Token might be expired (8 days by default)
- Login again to get a new token

### "Not a member of this room"
- You must be added to the room
- Create your own room or have someone add you

---

## API Endpoints Quick Reference

```bash
# Login
curl -X POST "http://localhost:8000/api/v1/login/access-token" \
  -d "username=admin@example.com&password=changethis"

# Create Room
curl -X POST "http://localhost:8000/api/v1/chat/rooms" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type": 2, "name": "My Room", "created_by": "USER_ID"}'

# Get Messages
curl "http://localhost:8000/api/v1/chat/rooms/ROOM_ID/messages" \
  -H "Authorization: Bearer YOUR_TOKEN"

# WebSocket
ws://localhost:8000/api/v1/ws/chat/ROOM_ID?token=YOUR_TOKEN
```

---

## Need Help?

1. Check [REALTIME_MESSAGING.md](../REALTIME_MESSAGING.md) for detailed documentation
2. Look at browser console for errors
3. Check backend logs for server-side errors
4. Ensure all services are running: `docker-compose ps`

**Happy Testing! 🎉**
