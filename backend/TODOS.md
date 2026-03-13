# Transport Security (MITM Defense)
Enforce **HTTPS only**.
TLS **1.2+ only**, disable legacy ciphers.
Enable **HSTS**.
Redirect HTTP -> HTTPS at the proxy.
No mixed content(WS must be WSS)

Websocket rule:
```
ws:// x
wss:// O
```

# Authentication and session security
Goal: Only authenticated users can connect and stay connected.

Short lived access tokens (5-15 mins)
Refresh tokens stored as:
    - HttpOnly
    - Secure
    - SameSite=Strict
Rotate refresh tokens on every use
Revoke tokens on logout

Token claims must include:
```
sub -> user_id
iat -> issued at
exp -> expiry
aud -> chat-service
```

# Authorization (Prevent unauthorized reads)
Goal: Even authenticated users cannot read others' messages.

Enforce **object level authorization**
Validate:
    - user is a member of the room
    - user is allowed ot send/read messages
Never trust room IDs from client

Server side check:
user_id ∈ room.members
```
# Websocket security (Most Attacked area)
Goal: Prevent hijacking, replay and room intrusion.

Authenticate before accepting WebSocket.
Reject unauthenticated socket upgrades.
Bind socket session to:
    - user_id
    - Device/session ID
Close socket on token expiry
Validate message schema strictly

Example flow:
1. Client sends token.
2. Server validates token.
3. Server validates room access
4. Server upgrades connection

# Message Encryption (At Rest & Optional E2EE)
Minimum(Required)
Encrypt messages at rest
Encrypt backups
Restrict DB access

# High Security (Optional but Strong)
End to end Encryption:
    - Server never sees plaintext
    - Per-conversation keys
    - Forward secrecy

Trade-off:
E2EE complicates moderation and search

# Message integrity and Replay Protection
Goal: Messages cannot be altered or replayed.

Message includes:
    - message_id (UUID)
    - timestamp
    - sender_id

Reject duplicate message IDs