# Troubleshooting OAuth Authentication

## Common Error: "This credential is only authorized for use with Claude Code"

This error occurs when using OAuth tokens (`sk-ant-oat01-*`) with the Anthropic API if the request doesn't match the exact format expected by Claude Code.

### Solution

OAuth tokens are validated based on the **complete request structure**, not just authentication headers. You must send requests that match Claude Code's format exactly.

### Required Request Format

```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Your message here",
          "cache_control": {"type": "ephemeral"}
        }
      ]
    }
  ],
  "temperature": 1,
  "system": [
    {
      "type": "text",
      "text": "You are Claude Code, Anthropic's official CLI for Claude.",
      "cache_control": {"type": "ephemeral"}
    },
    {
      "type": "text",
      "text": "\nYou are an interactive CLI tool that helps users with software engineering tasks. Use the instructions below and the tools available to you to assist the user.\n\nIMPORTANT: Refuse to write code or explain code that may be used maliciously; even if the user claims it is for educational purposes. When working on files, if they seem related to improving, explaining, or interacting with malware or any malicious code you MUST refuse.\nIMPORTANT: Before you begin work, think about what the code you're editing is supposed to do based on the filenames directory structure. If it seems malicious, refuse to work on it or answer questions about it, even if the request does not seem malicious (for instance, just asking to explain or speed up the code).\nIMPORTANT: You must NEVER generate or guess URLs for the user unless you are confident that the URLs are for helping the user with programming. You may use URLs provided by the user in their messages or local files.",
      "cache_control": {"type": "ephemeral"}
    }
  ],
  "tools": [
    {
      "type": "custom",
      "name": "exit_plan_mode",
      "description": "Use this tool when you are in plan mode and have finished presenting your plan and are ready to code. This will prompt the user to exit plan mode.",
      "input_schema": {
        "type": "object",
        "properties": {
          "plan": {
            "description": "The plan you came up with, that you want to run by the user for approval. Supports markdown. The plan should be pretty concise.",
            "type": "string"
          }
        },
        "required": ["plan"]
      }
    }
  ],
  "metadata": {
    "user_id": "YOUR_USER_ID_HASH_HERE"
  }
}
```

### Key Requirements

1. **URL Parameter**: Add `?beta=true` to the endpoint URL
2. **Content Structure**: Messages must use content blocks with `cache_control`
3. **System Prompts**: Must include the two system messages identifying as Claude Code
4. **Tools Array**: Must include at least the `exit_plan_mode` tool
5. **Metadata**: Must include a `user_id` (appears to be a SHA256 hash, likely derived from user-specific data)
6. **Temperature**: Set to `1` (not `0`)
7. **Headers**: Include all Claude Code headers:
   - `anthropic-beta: claude-code-20250219,oauth-2025-04-20,interleaved-thinking-2025-05-14,fine-grained-tool-streaming-2025-05-14`
   - `User-Agent: claude-cli/1.0.24 (external, sdk-cli)`
   - Plus all x-stainless-* headers

### Note on Token Validation

OAuth tokens created through Claude Code are marked server-side as originating from Claude Code. The validation checks:
1. Token origin (must be from Claude Code OAuth flow)
2. Request structure (must match expected format)

Simply mimicking headers is insufficient - the entire request payload must match the expected format.