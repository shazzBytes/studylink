#!/bin/bash

# Quick Test Script for Real-Time Messaging
# This script will help you test the WebSocket chat functionality

set -e

API_BASE="http://localhost:8000/api/v1"

echo "🚀 StudyLink Real-Time Messaging Test Script"
echo "============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Login
echo -e "${BLUE}Step 1: Login${NC}"
read -p "Enter email (default: admin@example.com): " EMAIL
EMAIL=${EMAIL:-admin@example.com}

read -sp "Enter password (default: changethis): " PASSWORD
PASSWORD=${PASSWORD:-changethis}
echo ""

echo "Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "${API_BASE}/login/access-token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=${EMAIL}&password=${PASSWORD}")

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    echo -e "${GREEN}✅ Login successful!${NC}"
    echo "Token: ${TOKEN:0:50}..."
else
    echo -e "${RED}❌ Login failed!${NC}"
    echo "$LOGIN_RESPONSE"
    exit 1
fi

echo ""

# Step 2: Get user info
echo -e "${BLUE}Step 2: Getting user info${NC}"
USER_RESPONSE=$(curl -s -X POST "${API_BASE}/login/test-token" \
  -H "Authorization: Bearer ${TOKEN}")

USER_ID=$(echo "$USER_RESPONSE" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
USER_EMAIL=$(echo "$USER_RESPONSE" | grep -o '"email":"[^"]*' | cut -d'"' -f4)

echo -e "${GREEN}✅ User ID: ${USER_ID}${NC}"
echo ""

# Step 3: Create or use existing room
echo -e "${BLUE}Step 3: Room Setup${NC}"
read -p "Do you want to create a new room? (y/n, default: y): " CREATE_ROOM
CREATE_ROOM=${CREATE_ROOM:-y}

if [[ "$CREATE_ROOM" == "y" ]]; then
    read -p "Enter room name (default: Test Chat Room): " ROOM_NAME
    ROOM_NAME=${ROOM_NAME:-Test Chat Room}
    
    echo "Creating room..."
    ROOM_RESPONSE=$(curl -s -X POST "${API_BASE}/chat/rooms" \
      -H "Authorization: Bearer ${TOKEN}" \
      -H "Content-Type: application/json" \
      -d "{\"type\": 2, \"name\": \"${ROOM_NAME}\", \"created_by\": \"${USER_ID}\"}")
    
    ROOM_ID=$(echo "$ROOM_RESPONSE" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
    echo -e "${GREEN}✅ Room created!${NC}"
    echo "Room ID: ${ROOM_ID}"
else
    read -p "Enter existing room ID: " ROOM_ID
fi

echo ""

# Step 4: Instructions for WebSocket testing
echo -e "${YELLOW}========================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
echo "Your credentials:"
echo "  Token: ${TOKEN}"
echo "  Room ID: ${ROOM_ID}"
echo "  User ID: ${USER_ID}"
echo ""
echo -e "${BLUE}Now you can test in 3 ways:${NC}"
echo ""
echo "1️⃣  ${YELLOW}Using the HTML Test Client:${NC}"
echo "   - Open: backend/test_websocket.html in your browser"
echo "   - The page has built-in login and room creation"
echo "   - Or paste these values:"
echo "     Token: ${TOKEN}"
echo "     Room ID: ${ROOM_ID}"
echo ""
echo "2️⃣  ${YELLOW}Using wscat (terminal WebSocket client):${NC}"
echo "   Install: npm install -g wscat"
echo "   Connect: wscat -c \"ws://localhost:8000/api/v1/ws/chat/${ROOM_ID}?token=${TOKEN}\""
echo "   Send message: {\"type\": \"message\", \"content\": \"Hello!\"}"
echo ""
echo "3️⃣  ${YELLOW}Using Python:${NC}"
echo "   Install: pip install websockets"
echo "   Run: python3 - <<EOF"
echo "import asyncio, websockets, json"
echo "async def test():"
echo "    uri = 'ws://localhost:8000/api/v1/ws/chat/${ROOM_ID}?token=${TOKEN}'"
echo "    async with websockets.connect(uri) as ws:"
echo "        await ws.send(json.dumps({'type': 'message', 'content': 'Hello from Python!'}))"
echo "        msg = await ws.recv()"
echo "        print(msg)"
echo "asyncio.run(test())"
echo "EOF"
echo ""
echo -e "${BLUE}To test with multiple users:${NC}"
echo "  - Open the HTML file in multiple browser windows/tabs"
echo "  - Or run this script again in another terminal"
echo ""
echo "Happy testing! 🎉"
