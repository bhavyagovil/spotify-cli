from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.history import InMemoryHistory

from core.cli_chat import SpotifyChat


class CliApp:
    def __init__(self, agent: SpotifyChat):
        self.agent = agent
        self.playlists = []

        self.history = InMemoryHistory()
        self.session = PromptSession(
            history=self.history,
            style=Style.from_dict(
                {
                    "prompt": "#aaaaaa",
                }
            ),
        )

    async def initialize(self):
        try:
            self.playlists = await self.agent.list_playlists()
        except Exception as e:
            print(f"Error loading playlists: {e}")

    async def run(self):
        while True:
            try:
                user_input = await self.session.prompt_async("> ")
                if not user_input.strip():
                    continue

                response = await self.agent.run(user_input)
                print(f"\n{response}\n")

            except KeyboardInterrupt:
                break
