
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from pydantic import Field
from mcp.server.fastmcp import FastMCP
import os

load_dotenv()

scope = "user-read-playback-state,user-modify-playback-state,playlist-read-private,playlist-read-collaborative"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope=scope
))

mcp = FastMCP("SpotifyMCP", log_level="ERROR")


def search_track(query):
    results = sp.search(query, type="track", limit=1)
    items = results['tracks']['items']
    return items[0] if items else None


@mcp.tool(
    name="play_track",
    description="Search for a track and play it immediately"
)
def cmd_play(query: str = Field(description="Track name or search query")):
    track = search_track(query)
    if not track:
        return f"No track found for: {query}"
    sp.add_to_queue(track['uri'])
    sp.next_track()
    return f"Playing: {track['name']} by {track['artists'][0]['name']}"


@mcp.tool(
    name="queue_track",
    description="Search for a track and add it to the queue"
)
def cmd_queue(query: str = Field(description="Track name or search query")):
    track = search_track(query)
    if not track:
        return f"No track found for: {query}"
    sp.add_to_queue(track['uri'])
    return f"Added to queue: {track['name']} by {track['artists'][0]['name']}"


@mcp.tool(
    name="shuffle_playlist",
    description="Find a playlist in your Spotify library and shuffle play it"
)
def cmd_playlist(name: str = Field(description="Playlist name or partial name")):
    query = name.lower()
    all_playlists = []
    batch = sp.current_user_playlists(limit=50)
    while batch:
        all_playlists.extend(batch['items'])
        batch = sp.next(batch) if batch['next'] else None
    matches = [p for p in all_playlists if query in p['name'].lower()]
    if not matches:
        return f"No playlist found in your library for: {name}"
    playlist = matches[0]
    sp.shuffle(True)
    sp.start_playback(context_uri=playlist['uri'])
    return f"Shuffling playlist: {playlist['name']}"


@mcp.tool(
    name="play_album",
    description="Search for an album and play it from the start"
)
def cmd_album(query: str = Field(description="Album name or search query")):
    results = sp.search(query, type="album", limit=1)
    items = results['albums']['items']
    if not items:
        return f"No album found for: {query}"
    album = items[0]
    sp.shuffle(False)
    sp.start_playback(context_uri=album['uri'])
    return f"Playing album: {album['name']} by {album['artists'][0]['name']}"


@mcp.tool(
    name="toggle_playback",
    description="Pause if playing, resume if paused"
)
def cmd_toggle():
    current = sp.current_playback()
    if current and current['is_playing']:
        sp.pause_playback()
        return "Paused"
    sp.start_playback()
    return "Resumed"


@mcp.tool(
    name="next_track",
    description="Skip to the next track"
)
def cmd_next():
    sp.next_track()
    return "Skipped to next track"


@mcp.tool(
    name="current_track",
    description="Get the currently playing track"
)
def cmd_curr():
    current = sp.current_playback()
    if not current or not current['item']:
        return "Nothing playing"
    track = current['item']
    return f"{track['name']} by {track['artists'][0]['name']} — {track['album']['name']}"


@mcp.resource(
    "spotify://playlists",
    mime_type="application/json"
)
def list_playlists() -> list[str]:
    all_playlists = []
    batch = sp.current_user_playlists(limit=50)
    while batch:
        all_playlists.extend(batch['items'])
        batch = sp.next(batch) if batch['next'] else None
    return [p['name'] for p in all_playlists]


if __name__ == "__main__":
    mcp.run(transport="stdio")
