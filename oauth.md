# Claude/Anthropic OAuth Authentication Flow

## Overview
This document details the OAuth 2.0 PKCE flow used by Claude Code CLI to authenticate with Anthropic's services.

## OAuth Configuration
- **Client ID**: `9d1c250a-e61b-44d9-88ed-5944d1962f5e`
- **Redirect URI**: `http://localhost:54545/callback` (must be whitelisted)
- **PKCE Method**: S256
- **Scopes**: `org:create_api_key user:profile user:inference`

## Authentication Flow

### 1. Authorization Request
Generate OAuth authorization URL with PKCE parameters:

```
GET https://claude.ai/oauth/authorize
```

**Parameters:**
- `code=true`
- `client_id=9d1c250a-e61b-44d9-88ed-5944d1962f5e`
- `response_type=code`
- `redirect_uri=http://localhost:54545/callback` (URL encoded)
- `scope=org:create_api_key user:profile user:inference`
- `code_challenge=<base64-url-encoded-sha256-hash>`
- `code_challenge_method=S256`
- `state=<random-state-value>`

### 2. Authorization Callback
After user authorization, OAuth server redirects to callback with authorization code:

```
POST http://localhost:54545/callback?code=<auth_code>&state=<state_value>
```

Server responds with redirect to success page:
```
HTTP 302
Location: https://console.anthropic.com/oauth/code/success?app=claude-code
```

### 3. Token Exchange
Exchange authorization code for access token:

```
POST https://console.anthropic.com/v1/oauth/token
Content-Type: application/json
```

**Body:**
```json
{
  "grant_type": "authorization_code",
  "code": "<authorization_code>",
  "redirect_uri": "http://localhost:54545/callback",
  "client_id": "9d1c250a-e61b-44d9-88ed-5944d1962f5e",
  "code_verifier": "<pkce_code_verifier>",
  "state": "<state_value>"
}
```

**Response:**
```json
{
  "token_type": "Bearer",
  "access_token": "sk-ant-oat01-...",
  "expires_in": 28800,
  "refresh_token": "sk-ant-ort01-...",
  "scope": "user:inference user:profile",
  "organization": {
    "uuid": "<org_uuid>",
    "name": "<org_name>"
  },
  "account": {
    "uuid": "<account_uuid>",
    "email_address": "<email>"
  }
}
```

### 4. Profile Verification
Verify successful authentication by fetching user profile:

```
GET https://api.anthropic.com/api/oauth/profile
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "account": {
    "uuid": "<account_uuid>",
    "full_name": "<full_name>",
    "display_name": "<display_name>",
    "email": "<email>",
    "has_claude_max": true,
    "has_claude_pro": false
  },
  "organization": {
    "uuid": "<org_uuid>",
    "name": "<org_name>",
    "organization_type": "claude_max",
    "billing_type": "stripe_subscription",
    "rate_limit_tier": "default_claude_max_5x"
  }
}
```

### 5. Role Information
Fetch user roles and permissions:

```
GET https://api.anthropic.com/api/oauth/claude_cli/roles
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "organization_uuid": "<org_uuid>",
  "organization_name": "<org_name>",
  "organization_role": "admin",
  "workspace_uuid": null,
  "workspace_name": null,
  "workspace_role": null
}
```

## Token Details
- **Access Token Format**: `sk-ant-oat01-...`
- **Refresh Token Format**: `sk-ant-ort01-...`
- **Token Expiry**: 28800 seconds (8 hours)
- **Token Type**: Bearer

## API Endpoints
- **Authorization**: `https://claude.ai/oauth/authorize`
- **Token Exchange**: `https://console.anthropic.com/v1/oauth/token`
- **Profile**: `https://api.anthropic.com/api/oauth/profile`
- **Roles**: `https://api.anthropic.com/api/oauth/claude_cli/roles`

## Security Notes
- Uses PKCE (Proof Key for Code Exchange) for enhanced security
- State parameter prevents CSRF attacks
- Tokens have limited lifespan (8 hours)
- Redirect URI must be exactly `http://localhost:54545/callback`