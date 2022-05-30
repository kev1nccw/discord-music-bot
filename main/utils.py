class NoVoiceChannelException(Exception):
    pass


class AudioNotFoundException(Exception):
    pass


class GetSourceErrorException(Exception):
    pass


class ExtractYouTubeException(Exception):
    pass


class ExtractSpotifyException(Exception):
    pass


class NoSpotifyAuthException(Exception):
    pass


class InvalidSpotifyAuthException(Exception):
    pass

class Audio:
    def __init__(self, title, url, loop=False):
        self.title = title
        self.url = url
        self.loop = loop

    def __str__(self):
        if self.loop:
            return f"{self.title} (looping)"
        else:
            return self.title

    def set_loop(self, loop):
        self.loop = loop
