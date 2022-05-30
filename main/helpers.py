import youtube_dl
from discord import FFmpegOpusAudio
from discord.utils import get

from main.search import *
from main.utils import *


YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


async def permission_check(bot, ctx):
    if ctx.message.author.voice == None:
        raise NoVoiceChannelException
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    return channel, voice


class AudioHandler:
    def create_audio(arg, loop=False):
        # Get audio url
        if is_youtube_url(arg):
            url = arg
        else:
            result = search_song(arg)
            if result is None:
                raise AudioNotFoundException
            url = result

        # Get audio title
        title = get_title(url)
        if title is None:
            raise AudioNotFoundException

        return Audio(title, url, loop)

    def get_audio_source(audio):
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                ydl.cache.remove()
                info = ydl.extract_info(audio.url, download=False)
                return FFmpegOpusAudio(info["url"], **FFMPEG_OPTIONS)
            except youtube_dl.utils.DownloadError as e:
                print(e)
                raise GetSourceErrorException


class InputHandler:
    def handle_input(arg):
        if InputHandler.is_playlist(arg):
            try:
                items = extract_playlist(arg)
                return items
            except Exception as e:
                raise (e)
        elif InputHandler.is_spotify_track(arg):
            try:
                return [extract_track(arg)]
            except Exception as e:
                raise (e)
        else:
            return [arg]

    def is_playlist(url):
        return (
            url.startswith("https://www.youtube.com/playlist?list=")
            or url.startswith("www.youtube.com/playlist?list=")
            or url.startswith("https://open.spotify.com/playlist/")
            or url.startswith("open.spotify.com/playlist/")
        )

    def is_spotify_track(url):
        return url.startswith("https://open.spotify.com/track/") or url.startswith(
            "open.spotify.com/track/"
        )
