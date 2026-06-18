from core.chat import Chat
from core.claude import Claude
from mcp_client import MCPClient


class SpotifyChat(Chat):
    def __init__(
        self,
        spotify_client: MCPClient,
        clients: dict[str, MCPClient],
        claude_service: Claude,
    ):
        super().__init__(clients=clients, claude_service=claude_service)
        self.spotify_client = spotify_client

    async def list_playlists(self) -> list[str]:
        return await self.spotify_client.read_resource("spotify://playlists")

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": query})
