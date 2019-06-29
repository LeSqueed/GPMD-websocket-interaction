# GPMD-websocket-interaction
A Python script that allows you to send websocket messages to the unnofficial Google Play Music Desktop Player.
You can control the unnofficial Google Play Music Desktop Player through a CLI with this.

## Dependencies

Outside of the default modules this makes use of "websockets" which you can install with "pip install websockets".

## How to set it up

Make sure you have the unnofficial Google Play Music Desktop Player running for this process.
We first need to get authorisation to send commands through the websocket interface, for this we are going to run Get_Token.py.

After running Get_Token.py you should see that Google Play Music Desktop Player is showing a code, enter this code in the CLI when asked to and press enter. This should have created a new file called "key.json".
Now you are ready to use the actual script to control your music.

## A few examples

```Send_Command.py playback playPause```

This toggles between play and pause.

```Send_Command.py volume decreaseVolume```

This decreases the volume in steps of 5.

For a documentation on what commands are possible you can take a look at this page:
https://github.com/gmusic-utils/gmusic.js

For an explanation on how the websocket used works read the following page:
https://github.com/MarshallOfSound/Google-Play-Music-Desktop-Player-UNOFFICIAL-/blob/master/docs/PlaybackAPI_WebSocket.md
