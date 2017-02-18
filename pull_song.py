#!/usr/bin/env python3.6
import sqlite3
from subprocess import call
"""DOWNLOADS THE YOTUBE VIDEO AT THE URL"""
command = "youtube-dl --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=pZO-WvZHp8M -c"
call(command.split(), shell=False)


