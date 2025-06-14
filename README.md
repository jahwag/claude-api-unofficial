# Claude API Unofficial

Documentation of Anthropic / Claude APIs.

## APIs Documented

### Claude Code CLI
- [`claude-code/`](claude-code/) - Anthropic API used by Claude Code
  - OAuth authentication flow
  - API endpoints specification
  - **NEW**: [Troubleshooting OAuth authentication](claude-code/troubleshooting.md)

### Claude.ai Web
- [`claude-web/`](claude-web/) - Web API used by claude.ai

## Recent Findings

### OAuth Token Authentication (2025-06-14)
Successfully reverse-engineered the request format required for OAuth token authentication.
OAuth tokens are validated based on the complete request structure, not just headers.
See [troubleshooting guide](claude-code/troubleshooting.md) for details.

## Disclaimer

Unofficial documentation created for educational purposes. Not affiliated with Anthropic.

## Contributing

Contributions welcome.