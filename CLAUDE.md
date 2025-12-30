# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Browser Automation Stealth - Anti-detection browser automation toolkit for AI agents and Claude Code integration. Uses Camoufox (Firefox with C++ fingerprint injection) and optionally Ulixee Hero (Chrome with native human behavior).

## Key Commands

```bash
# Verify installation
python3 test_instalacion.py

# Run Python browser utility directly
python3 src/python/camoufox_browser.py <url> [--visible] [--text] [--links] [--screenshot path]

# Run parallel browser test (3 instances)
python3 src/python/test_parallel.py

# Start MCP server manually (usually auto-started by Claude Code)
python3 mcp-server/camoufox_mcp_server.py

# Docker
docker build -t browser-stealth .
docker run -it --rm browser-stealth python3 examples/uso_basico.py
```

## Architecture

### MCP Server Integration
- `mcp-server/camoufox_mcp_server.py` - MCP server exposing browser control tools to Claude Code
- Configured in `~/.mcp.json` or `~/.claude/settings.json` under `mcpServers.camoufox`
- Tools available: `browser_navigate`, `browser_click`, `browser_fill`, `browser_press`, `browser_screenshot`, `browser_extract`, `browser_get_content`, `browser_scroll`, `browser_wait`, `browser_close`, `browser_status`

### Python Browser Module
- `src/python/camoufox_browser.py` - Main utility with `browse()`, `browse_async()`, and `search_mercadolibre()` functions
- Uses `pyvirtualdisplay` for background mode (virtual X display)
- Supports custom actions via callback functions

### Visibility Modes
| Mode | Python Setting | Description |
|------|----------------|-------------|
| Visible | `headless=False` | Browser window visible |
| Background | `headless="virtual"` | Uses Xvfb virtual display (less detectable than pure headless) |

### Dependencies
- **Required**: `camoufox[geoip]`, `mcp`, `pyvirtualdisplay`
- **System**: `xvfb` for background mode
- **Optional**: Node.js 18+ and `@ulixee/hero-playground` for Hero alternative

## Development Patterns

### Browser Session State
The MCP server maintains a singleton `BrowserState` class that persists across tool calls. The browser is lazy-initialized on first `browser_navigate` and must be explicitly closed with `browser_close`.

### Error Handling
All MCP tool calls return `TextContent` with either success messages or error strings prefixed with "Error:". Tools check for browser initialization before executing.

### Background Mode
When `visible=False`, the MCP server starts a virtual display (1920x1080) via `pyvirtualdisplay.Display`. This requires Xvfb installed on the system.
