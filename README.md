# ScHoolboy-Queue
VTHacks IV -- Team Fully Torged
### Team: FULLY TORGED

## Purpose
Every single person has a unique taste in music, so this can sometimes be a point of frustration when you are with other people and only listening to music that they like.

Often, the solution is to have something akin to the Spotify queue. One person has control of the music but others can request songs to be added to be listened to at a later data.

While this is often manageable between friends, there are still several pain points:
1. Someone often needs to give up their phone to play music from
..* If they keep their phone locked they will need to be continually asked to unlock it
1. The content is limited by the library of the streaming provider
1. Generally only a single person can queue up music at a time
1. Everyone who has access to the queue has the ability to rearrage or remove anything they want
1. The sound system is frequently located off to the side

The goal of ScHoolboy Queue (sHouts to my mans) is to provide a remotely hosted, collaborative queue/playlist that puts the choice of music in the hands of the crowd, while still maintaining a level of control for the person hosting

With a central web server that communicates with distributed nodes in the form of `rooms,` ScHoolboyQueue allows a user to play a continuous stream of music straight from YouTube.

## Usage
The application consists of two integral parts:
1. [A centralized web site](www.ScHoolboyQueue.org/) used to manage the queues for the individual rooms
1. Distributed rooms/nodes that handle the playing on the music 

### Running

Alongside the code for the webapp, this repo also contains the cli application to play music and create rooms. Get started with the cli as follows

```bash
# Clone the repo locally
git clone git@github.com:DanielSBrown/ScHoolboy-Queue.git

# Download the requirements using Python's pip package manager
# Usage of a virtual environment for dependency management is highly recommended
pip install -r requirements.txt

# Get the cli working globally
cd cliBoy_Queue
pip install .

# In order to create a new room but not begin playing immediately
cliboy_queue create

# In order to delete a room
cliboy_queue delete ROOM_ID

# In order to create a room and begin playing from it
cliboy_queue connect
# Or connect to an already created room
cliboy_queue connect --room ROOM_ID

# The CLI expects an environment variable $SERVER_ADDR to know where to create the room
# If not hosting your own server, this should be www.ScHoolboyQueue.org
```

### Requirements

* Python 3.6
* VLC Media Player

Opportunities For Growth
------

1. Improved user system for moderation of queues and albility to grant moderation powers
1. Ability to rearrange queue, beyond just deleting items
1. Ability to save and share playlists
1. Package cli to distribute with pip

# Disclaimer
The Team who built ScHoolboy Queue do not condone any use of this application to illegally download licensed music
