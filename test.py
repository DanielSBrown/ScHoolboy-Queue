from pygame import mixer
import pygame
import time
import youtube_dl
import vlc
import os
from mutagen.mp3 import MP3

"""THIS FILE IS PURELY FOR TESTING HOW AUDIO WORKS. """
"""TODO: FIGURE OUT HOW TO QUERY YOUTUBE"""


if __name__ == "__main__":
    audio = MP3("/Users/danielbrown/ScHoolboy-Queue/Burrito Van - Parry Gripp-pZO-WvZHp8M.mp3")
    print(audio.info.length)
    p = vlc.MediaPlayer("file:///Users/danielbrown/ScHoolboy-Queue/Burrito Van - Parry Gripp-pZO-WvZHp8M.mp3")
    p.play()
    time.sleep(audio.info.length)
    p.stop()
    os.remove('/Users/danielbrown/ScHoolboy-Queue/Burrito Van - Parry Gripp-pZO-WvZHp8M.mp3')
