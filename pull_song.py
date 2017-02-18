#!/usr/bin/env python3.6
import sqlite3
from subprocess import call

command = "youtube-dl https://www.youtube.com/watch?v=dQw4w9WgXcQ -c"
call(command.split(), shell=False)


