import asyncio
import random
from discord import Activity, Game, ActivityType
from discord.ext import commands

import main.config as config
from main.helpers import AudioHandler, InputHandler, permission_check
from main.utils import *


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    async def play_audio(self, voice, ctx, pop: bool):
        if pop:
            self.queue.pop(0)

        if not self.queue:
            # Return if queue is empty
            await self.bot.change_presence(
                activity=Activity(name=config.READY_STATUS, type=ActivityType.watching),
            )
            return
        audio = self.queue[0]

        try:
            audio_source = AudioHandler.get_audio_source(audio)
            voice.play(
                audio_source,
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.play_audio(voice, ctx, not audio.loop == True), self.bot.loop
                ),
            )
            await self.bot.change_presence(activity=Game(name=audio.title))
            await ctx.send(config.AUDIO_PLAY(audio))
        except GetSourceErrorException:
            await ctx.send(config.GET_SOURCE_ERROR(audio))
            self.play_song(voice, ctx, True)
        finally:
            await asyncio.sleep(600)
            if not self.queue:
                await self.bot.change_presence(
                    activity=CustomActivity(name=config.READY_STATUS)
                )
                await voice.disconnect()

    async def process_urls(self, ctx, urls, count=0):
        for song_url in urls:
            song = AudioHandler.create_audio(song_url)
            if song:
                self.queue.append(song)
                count += 1
                await ctx.send(f"{song} has been added to queue!", delete_after=0.1)
        await ctx.send(f"Added {count} songs to the queue!")

    async def handle_exception(self, ctx, e):
        if type(e) == NoVoiceChannelException:
            await ctx.send(config.NO_VOICE_CHANNEL)
        elif type(e) == AudioNotFoundException:
            await ctx.send(config.AUDIO_NOT_FOUND)
        elif type(e) == NoSpotifyAuthException:
            await ctx.send(config.NO_SPOTIFY_AUTH)
        elif type(e) == InvalidSpotifyAuthException:
            await ctx.send(config.INVALID_SPOTIFY_AUTH)
        elif type(e) == ExtractYouTubeException:
            await ctx.send(config.YOUTUBE_PLAYLIST_ERROR)
        elif type(e) == ExtractSpotifyException:
            await ctx.send(config.SPOTIFY_PLAYLIST_ERROR)
        else:
            print(e)
            await ctx.send(config.UNKNOWN_ERROR)

    """
    Control-related commands
    """

    @commands.command(name="play", aliases=["add"])
    async def play(self, ctx, *args):
        try:
            # Connect to user's voice channel
            channel, voice = await permission_check(self.bot, ctx)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()

            # Handle argument
            arg = " ".join(args)
            items = InputHandler.handle_input(arg)
            if len(items) > 1:
                # Playlist
                if not self.queue:
                    # Play the first audio while processing others if queue is empty
                    audio = AudioHandler.create_audio(items.pop(0))
                    self.queue.append(audio)
                    await asyncio.gather(
                        self.play_audio(voice, ctx, False),
                        self.process_urls(ctx, items, count=1),
                    )
                else:
                    await self.process_urls(ctx, items)
            else:
                # Track
                audio = AudioHandler.create_audio(items[0])
                self.queue.append(audio)

                if len(self.queue) == 1:
                    # Play if queue is empty
                    await self.play_audio(voice, ctx, False)
                else:
                    # Add to queue
                    await ctx.send(config.ADDED_TO_QUEUE(audio))
        except Exception as e:
            await self.handle_exception(ctx, e)

    @commands.command(name="pause", aliases=["stop"])
    async def pause(self, ctx):
        try:
            _, voice = await permission_check(self.bot, ctx)
            if voice and voice.is_playing():
                voice.pause()
                await ctx.send(config.AUDIO_PAUSE(self.queue[0]))
            else:
                await ctx.send(config.AUDIO_PAUSE_FAIL)
        except Exception as e:
            await self.handle_exception(ctx, e)

    @commands.command(name="resume", aliases=["continue"])
    async def resume(self, ctx):
        try:
            _, voice = await permission_check(self.bot, ctx)
            if voice and not voice.is_playing():
                voice.resume()
                await ctx.send(config.AUDIO_RESUME(self.queue[0]))
            else:
                await ctx.send(config.AUDIO_RESUME_FAIL)
        except Exception as e:
            await self.handle_exception(ctx, e)

    @commands.command(name="skip", aliases=["next"])
    async def skip(self, ctx):
        try:
            _, voice = await permission_check(self.bot, ctx)
            if self.queue:
                self.queue[0].set_loop(False)  # Ensure not looping
                if voice:
                    voice.stop()
                    await ctx.send(config.AUDIO_SKIP(self.queue[0]))
            else:
                await ctx.send(config.SKIP_FAIL)
        except Exception as e:
            await self.handle_exception(ctx, e)

    @commands.command(name="front")
    async def front(self, ctx, *args):
        try:
            await permission_check(self.bot, ctx)

            arg = " ".join(args)
            if InputHandler.is_playlist(arg):
                await ctx.send(config.NOT_SUPPORTED)
            elif not self.queue:
                await ctx.send(config.FRONT_FAIL)
            else:
                items = InputHandler.handle_input(arg)
                audio = AudioHandler.create_audio(items[0])
                self.queue.insert(1, audio)
                await ctx.send(config.ADDED_TO_QUEUE(audio))
        except Exception as e:
            await self.handle_exception(ctx, e)

    @commands.command(name="loop")
    async def loop(self, ctx, *args):
        try:
            # Connect to user's voice channel
            channel, voice = await permission_check(self.bot, ctx)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()

            # Handle argument
            arg = " ".join(args)
            if InputHandler.is_playlist(arg):
                await ctx.send(config.NOT_SUPPORTED)
            else:
                items = InputHandler.handle_input(arg)
                audio = AudioHandler.create_audio(items[0], loop=True)
                self.queue.append(audio)

                if len(self.queue) == 1:
                    # Play if queue is empty
                    await self.play_audio(voice, ctx, False)
                else:
                    # Add to queue
                    await ctx.send(config.ADDED_TO_QUEUE(audio))
        except Exception as e:
            await self.handle_exception(ctx, e)

    """
    Queue-related commands
    """

    @commands.command(name="show", aliases=["list"])
    async def show(self, ctx):
        if self.queue:
            await ctx.send(config.QUEUE_SHOW(self.queue))
        else:
            await ctx.send(config.QUEUE_FAIL)

    @commands.command(name="remove", aliases=["delete"])
    async def remove(self, ctx, idx):
        try:
            _, _ = await permission_check(self.bot, ctx)
            idx = int(idx)
            if idx < len(self.queue):
                audio = self.queue.pop(idx)
                await ctx.send(config.QUEUE_REMOVE(audio))
            else:
                await ctx.send(config.REMOVE_FAIL)
        except Exception as e:
            await self.handle_exception(ctx, e)

    @commands.command(name="shuffle")
    async def shuffle(self, ctx):
        try:
            _, _ = await permission_check(self.bot, ctx)
            temp_queue = self.queue[1:]  # Ignore the playing audio
            random.shuffle(temp_queue)
            self.queue[1:] = temp_queue
            await ctx.send(config.QUEUE_SHUFFLE)
        except Exception as e:
            await self.handle_exception(ctx, e)

    @commands.command(name="clear")
    async def clear(self, ctx):
        try:
            _, voice = await permission_check(self.bot, ctx)
            if voice.is_playing():
                for _ in range(len(self.queue) - 1):
                    self.queue.pop()
            else:
                self.queue.clear()
            await ctx.send(config.QUEUE_CLEAR)
        except Exception as e:
            await self.handle_exception(ctx, e)
