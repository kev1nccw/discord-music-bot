import os

# System
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_PREFIX = os.getenv("BOT_PREFIX", "-")
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID", "")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET", "")

# Response
def ADDED_TO_QUEUE(audio):
    return f"{audio} has been added to the queue!"
def AUDIO_PLAY(audio):
    return f"**♫Now playing♫:** {audio.title}\n{audio.url}"
def AUDIO_PAUSE(audio):
    return f"Pausing {audio}..."
def AUDIO_RESUME(audio):
    return f"Resuming {audio}..."
def AUDIO_SKIP(audio):
    return f"Skipping {audio}..."
def QUEUE_SHOW(queue, n=11):
    message = f"**♫Now playing♫:**\n> {queue[0]}\n**Upcoming:**\n"
    for idx, song in enumerate(queue[1:n]):
        message += f"> {idx+1}. {song}\n"
    if len(queue) > n:
        message += f"...and {len(queue)-n} more"
    return message
def QUEUE_REMOVE(audio):
    return f"{audio} has been removed from the queue!"
QUEUE_SHUFFLE = "Queue shuffled!"
QUEUE_CLEAR = "Queue cleared!"

AUDIO_PAUSE_FAIL = "There is nothing I can pause!"
AUDIO_RESUME_FAIL = "There is nothing I can resume!"
SKIP_FAIL = "There is nothing I can skip!"
FRONT_FAIL = "The queue is empty! Use the `play` command instead!"
QUEUE_FAIL = "There is nothing in the queue!"
REMOVE_FAIL = "The index is not in the queue!"

# Exception
NO_VOICE_CHANNEL = "You need to be in a voice channel to run the command!"
AUDIO_NOT_FOUND = "Audio not found!"
def GET_SOURCE_ERROR(audio):
    return f"Error in playing {audio}!"
NO_SPOTIFY_AUTH = "No Spotify Auth found!"
INVALID_SPOTIFY_AUTH = "Invalid Spotify Auth!"
YOUTUBE_PLAYLIST_ERROR = "Error in playing the YouTube playlist"
SPOTIFY_PLAYLIST_ERROR = "Error in playing the Spotify playlist"
NOT_SUPPORTED = "Playlist is not supported in this command!"
UNKNOWN_ERROR = "Something went wrong..."

# Appearance
READY_STATUS = f"{BOT_PREFIX}help for help"

# Log
ON_READY = "Ready!"
BOT_TOKEN_NOT_FOUND = "Error: Discord bot token not found!"
SPOTIFY_TOKEN_NOT_FOUND = "Warning: Spotify client token not found!"

# Help
HELP = f"""
```
Command List:
{BOT_PREFIX}play [url/query] - Play the audio. If the bot is already playing, add it to the end of the queue.
{BOT_PREFIX}pause - Pause the current audio (if any).
{BOT_PREFIX}resume - Resume the current audio (if any).
{BOT_PREFIX}skip - Skip the current audio.
{BOT_PREFIX}front [url/query] - Add the audio to the front of the queue.
{BOT_PREFIX}loop [url/query] - Loop the audio.
{BOT_PREFIX}show - Show the queue.
{BOT_PREFIX}shuffle - Shuffle the queue.
{BOT_PREFIX}remove [idx] - Remove the specified item in the list.
{BOT_PREFIX}clear - Clear the queue.
{BOT_PREFIX}shutdown - Shut down the bot.
```
"""