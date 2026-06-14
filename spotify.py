import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

scope = "user-read-playback-state,user-modify-playback-state,playlist-read-private,playlist-read-collaborative"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope=scope
))


def search_track(query):
    results = sp.search(query, type="track", limit=1)
    items = results['tracks']['items']
    return items[0] if items else None


def cmd_play(arg):
    track = search_track(arg)
    if not track:
        print(f"No track found for: {arg}")
        return
    sp.add_to_queue(track['uri'])
    sp.next_track()
    print(f"Playing: {track['name']} by {track['artists'][0]['name']}")


def cmd_queue(arg):
    track = search_track(arg)
    if not track:
        print(f"No track found for: {arg}")
        return
    sp.add_to_queue(track['uri'])
    print(f"Added to queue: {track['name']} by {track['artists'][0]['name']}")


def cmd_playlist(arg):
    query = arg.lower()
    all_playlists = []
    batch = sp.current_user_playlists(limit=50)
    while batch:
        all_playlists.extend(batch['items'])
        batch = sp.next(batch) if batch['next'] else None
    matches = [p for p in all_playlists if query in p['name'].lower()]
    if not matches:
        print(f"No playlist found in your library for: {arg}")
        return
    playlist = matches[0]
    sp.shuffle(True)
    sp.start_playback(context_uri=playlist['uri'])
    print(f"Shuffling playlist: {playlist['name']}")


def cmd_album(arg):
    results = sp.search(arg, type="album", limit=1)
    items = results['albums']['items']
    if not items:
        print(f"No album found for: {arg}")
        return
    album = items[0]
    sp.shuffle(False)
    sp.start_playback(context_uri=album['uri'])
    print(f"Playing album: {album['name']} by {album['artists'][0]['name']}")


def cmd_toggle():
    current = sp.current_playback()
    if current and current['is_playing']:
        sp.pause_playback()
        print("Paused")
    else:
        sp.start_playback()
        print("Resumed")


def cmd_next():
    sp.next_track()


ARG_COMMANDS = {'p': cmd_play, 'q': cmd_queue, 'pl': cmd_playlist, 'pa': cmd_album}
NO_ARG_COMMANDS = {'x': cmd_toggle, 'n': cmd_next}

HELP = "Commands: p <song>, q <song>, pl <playlist>, pa <album>, x, n, quit"

while True:
    try:
        inp = input('> ').strip()
    except (EOFError, KeyboardInterrupt):
        break

    if not inp:
        continue

    cmd, _, arg = inp.partition(' ')

    if cmd == 'quit':
        break

    if cmd in ARG_COMMANDS:
        ARG_COMMANDS[cmd](arg)
    elif cmd in NO_ARG_COMMANDS:
        NO_ARG_COMMANDS[cmd]()
    else:
        print(HELP)
