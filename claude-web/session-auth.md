# Session Authentication

Extract `sessionKey` from claude.ai browser cookies.

```mermaid
sequenceDiagram
    participant User as User
    participant Browser as Web Browser
    participant ClaudeWeb as claude.ai
    participant Client as API Client
    participant API as api.claude.ai

    Note over User: 1. Manual Login
    User->>Browser: Open https://claude.ai
    Browser->>ClaudeWeb: GET /login
    ClaudeWeb->>Browser: Present login form
    User->>Browser: Enter credentials
    Browser->>ClaudeWeb: POST login credentials
    ClaudeWeb->>Browser: Set sessionKey cookie
    Note right of Browser: Cookie: sessionKey=sk-ant-[session_key]

    Note over User: 2. Extract Session Key
    User->>Browser: Open Developer Tools
    User->>Browser: Navigate to Application/Storage tab
    User->>Browser: Find sessionKey cookie value
    User->>Client: Configure with session key

    Note over Client: 3. API Access
    Client->>API: GET /organizations
    Note right of API: Cookie: sessionKey=sk-ant-[session_key]<br/>User-Agent: Mozilla/5.0...
    API->>Client: Organization data

    Client->>API: POST /organizations/{org_id}/chat_conversations/{chat_id}/completion
    Note right of API: Cookie: sessionKey=sk-ant-[session_key]<br/>Content-Type: application/json
    API-->>Client: SSE stream response
```

## Headers

```http
Cookie: sessionKey=sk-ant-sid01-1234567890abcdef...
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0
Content-Type: application/json
```

## Extraction

1. Login to https://claude.ai
2. F12 → Application → Cookies → https://claude.ai  
3. Copy `sessionKey` value