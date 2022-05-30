import re
import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch

import main.config as config
from main.utils import (
    ExtractSpotifyException,
    ExtractYouTubeException,
    InvalidSpotifyAuthException,
    NoSpotifyAuthException,
)


if config.SPOTIPY_CLIENT_ID == "":
    print(config.SPOTIFY_TOKEN_NOT_FOUND)
    sp = None
else:
    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            config.SPOTIPY_CLIENT_ID, config.SPOTIPY_CLIENT_SECRET
        )
    )


def is_youtube_url(argument):
    return argument.startswith(
        "https://www.youtube.com/watch?v="
    ) or argument.startswith("www.youtube.com/watch?v=")


def extract_playlist(url):
    if url.startswith("https://www.youtube.com/playlist?list=") or url.startswith(
        "www.youtube.com/playlist?list="
    ):
        # YouTube playlist
        try:
            r = requests.get(url)
            video_ids = set(re.findall(r"watch\?v=(\S{11})", r.text))
            urls = map(lambda id: f"https://www.youtube.com/watch?v={id}", video_ids)
            return list(urls)
        except Exception as e:
            print(e)
            raise ExtractYouTubeException
    else:
        # Spotify playlist
        try:
            if sp:
                uri = url.split("/")[-1].split("?")[0]
                titles = [
                    track["track"]["artists"][0]["name"] + " " + track["track"]["name"]
                    for track in sp.playlist_tracks(uri)["items"]
                ]
                return titles
            else:
                raise NoSpotifyAuthException
        except spotipy.oauth2.SpotifyOauthError:
            raise InvalidSpotifyAuthException
        except Exception as e:
            print(e)
            raise ExtractSpotifyException


def extract_track(url):
    # Spotify track
    try:
        if sp:
            uri = url.split("/")[-1].split("?")[0]
            track = sp.track(uri)
            return f"{track['artists'][0]['name']} {track['name']}"
        else:
            raise NoSpotifyAuthException
    except spotipy.oauth2.SpotifyOauthError:
        raise InvalidSpotifyAuthException
    except Exception as e:
        print(e)
        raise ExtractSpotifyException


def search_song(query: str):
    results = YoutubeSearch(query, max_results=1).to_dict()
    try:
        id = results[0]["id"]
        return f"https://www.youtube.com/watch?v={id}"
    except:
        return None


def get_title(url: str):
    try:
        r = requests.get(url)
        s = BeautifulSoup(r.text, features="html.parser")
        data = s.find("meta", itemprop="name")
        return data["content"]
    except:
        return None
