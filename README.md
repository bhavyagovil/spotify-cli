# Spotify CLI

A natural language Spotify controller powered by Claude. Type what you want to hear and Claude figures out what to play.

## How it works

Your message goes to Claude, which reads the available Spotify tools and decides what to do. You don't type commands — you just talk to it.

```
> play some sad indie songs
> queue bohemian rhapsody
> play the dark side of the moon
> shuffle my workout playlist
> what's playing?
> pause
```

## Prerequisites

- Python 3.10+
- Anthropic API key
- Spotify Premium account + Spotify app open on a device

## Setup

### 1. Configure environment variables

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=""
CLAUDE_MODEL="claude-sonnet-4-6"

SPOTIPY_CLIENT_ID=""
SPOTIPY_CLIENT_SECRET=""
SPOTIPY_REDIRECT_URI="http://localhost:8888/callback"
```

To get Spotify credentials, create an app at [developer.spotify.com](https://developer.spotify.com/dashboard).

### 2. Install dependencies

#### With uv (recommended)

```bash
pip install uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

#### Without uv

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3. Run

```bash
python main.py
```

On first run, Spotify will open a browser window to authorize the app.

## Project structure

```
mcp_server.py      # Spotify tools exposed via MCP
mcp_client.py      # Connects main.py to the MCP server
main.py            # Entry point — wires Claude, MCP client, and CLI together
core/
  claude.py        # Anthropic API wrapper
  chat.py          # Agentic loop (send → tool call → execute → repeat)
  cli_chat.py      # Spotify-specific chat (extends Chat)
  cli.py           # Interactive prompt (prompt_toolkit)
  tools.py         # Tool discovery and execution
```

## Available tools

| Tool | Description |
|---|---|
| `play_track` | Search for a track and play it immediately |
| `queue_track` | Add a track to the queue |
| `shuffle_playlist` | Find a playlist in your library and shuffle it |
| `play_album` | Search for an album and play it in order |
| `toggle_playback` | Pause or resume |
| `next_track` | Skip to next |
| `current_track` | Show what's playing |
