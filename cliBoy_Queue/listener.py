''' Meat of the application '''
from time import sleep, time
import youtube_dl
import requests
import vlc
from os import remove
# from mutagen.mp3 import MP3

YDL_OPTS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s',
}


def poll_and_wait(room, wait_time, api):
    '''
    This is the main body of the cli app.
    It will begin playing the first queued song and downloading the next queued
    Every $wait_time it will poll the server to check the queue
    If the current playing song has been removed, it will keep playing until the
        next has been downlaoded
    Whenever the current playing song has finished, it will send and update to
        the server, start playing the queued song, and download the next
    '''
    endpoint = '{}/queued/?room={}'.format(api, room)
    next_end = '{}/room/pop/'.format(api)
    playtime = 0
    initial = int(time())
    curr = None
    song = None
    queued = None
    next_song = ()
    file_name = None
    while True:
        if (time() - playtime < initial or curr is None) and (int(time()) - initial) % wait_time != 0:
            # If still playing, only update every X seconds
            sleep(1)
            continue
        sleep(1)
        queue = requests.get(endpoint).json()
        if not queue['current'] and song:
            # The queue was just made empty
            # Stop the current song and wait for more
            song.stop()
            remove(file_name)
            curr = None
            song = None
            playtime = 0
            continue
        elif not queue['current']:
            # The queue was already empty and nothing changed
            continue
        elif curr != queue['current'] and song:
            # The currently playing song was just removed from the queue
            song.stop()
            remove(file_name)
            if queued == queue['current']:
                # The next song is already downloaded
                file_name = next_song[0]
                song = play_song(file_name)
                initial = int(time())
                playtime = next_song[1]
                curr = queued
                queued = None
                next_song = None
                continue
            else:
                # We're gonna need to download the next song
                curr = None
                queued = None
                next_song = ()
                continue
        elif curr != queue['current']:
            # The queue was empty and it just got a new entry
            curr = queue['current']
            file_name, playtime = download_song(curr)
            song = play_song(file_name)
            initial = int(time())
            # TO DO: Don't let people queue up same song twice
            if not queue['next']:
                continue
            queued = queue['next']
            next_song = download_song(queued)
            continue
        elif queue['next'] and queued != queue['next']:
            # The pre-downloaded song is no longer in the queue
            queued = queue['next']
            next_song = download_song(queued)
            continue
        elif time() - playtime > initial:
            # The current song just ended
            song.stop()
            requests.post(next_end, data={'room': room})
            remove(file_name)
            if queued:
                # The next song is already downloaded
                file_name = next_song[0]
                song = play_song(next_song[0])
                initial = int(time())
                playtime = next_song[1]
                curr = queued
                queued = None
                next_song = ()
            continue


def play_song(name):
    """ Play the song """
    song = vlc.MediaPlayer(name)
    song.play()
    return song


def download_song(link):
    '''
    Use youtube-dl to download the songs to play
    '''
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        ydl.download([link])
        info = ydl.extract_info(link, download=False)
        return ('{}.mp3'.format(info['title']), info['duration'])
