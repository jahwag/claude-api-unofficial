# OAuth 2.0 PKCE Flow

OAuth authentication for Claude CLI.

**Client ID**: `9d1c250a-e61b-44d9-88ed-5944d1962f5e`  
**Redirect URI**: `http://localhost:54545/callback`  
**Scopes**: `org:create_api_key user:profile user:inference`

```mermaid
sequenceDiagram
    participant CLI as CLI Client
    participant Browser as User Browser
    participant Auth as claude.ai
    participant Token as console.anthropic.com
    participant API as api.anthropic.com

    CLI->>CLI: Generate PKCE challenge
    CLI->>Browser: Open authorization URL
    Browser->>Auth: GET /oauth/authorize
    Auth->>Browser: Present login form
    Browser->>Auth: User authorizes
    Auth->>Browser: Redirect with code
    Browser->>CLI: Authorization code
    CLI->>Token: POST /v1/oauth/token
    Token->>CLI: Access & refresh tokens
    CLI->>API: GET /api/oauth/profile
    API->>CLI: User profile
```

## PKCE Generation

```
code_verifier = base64url(random(43-128 chars))
code_challenge = base64url(sha256(code_verifier))
```

## Token Format

- **Access**: `sk-ant-oat01-...` (8 hours)
- **Refresh**: `sk-ant-ort01-...`