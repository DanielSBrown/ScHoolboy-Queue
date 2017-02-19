''' Meat of the application '''
from time import sleep, time
import youtube_dl
import requests
import vlc
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
    initial = time()
    curr = None
    song = None
    queued = None
    next_song = ()
    while True:
        if (time() - playtime) < initial and (time() - initial) % wait_time != 0:
            sleep(1)
            continue
        queue = requests.get(endpoint).json()
        if not queue['current']:
            sleep(1)
            continue
        elif curr != queue['current']:
            curr = queue['current']
            file_name, playtime = download_song(curr)
            print(file_name)
            song = play_song(file_name)
            initial = time()
            # TO DO: Don't let people queue up same song twice
            if not queue['next']:
                continue
            queued = queue['next']
            next_song = download_song(queued)
        else:
            song.stop()
            requests.post(next_end, data={'room': room})
            if queued:
                song = play_song(next_song[0])
                initial = time()
                playtime = next_song[1]



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
