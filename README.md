# GPMD-websocket-interaction
A Python script that allows you to send websocket messages to the unnofficial Google Play Music Desktop Player.
You can control the unnofficial Google Play Music Desktop Player through a CLI with this.

## Dependencies

Outside of the default modules this makes use of "websockets" which you can install with "pip install websocket-client".

## How to set it up

Make sure you have the unofficial Google Play Music Desktop Player running for this process.
To update the values in config.ini to correspond to what we need we execute the following command.

```Send_Command.py configure```

This will ask you for a few inputs. If you keep these inputs blank it will use the default values. After having entered the IP and Port of the websocket server it will ask for a key. This key will be shown in the Google Play Music Desktop Player, enter this code in the CLI when asked to and press enter.
Now you are ready to use the actual script to control your music, this can now be done by sending specific commands and there is no further requirement to interact with it in the CLI.

## A few examples

```Send_Command.py playback playPause```

This toggles between play and pause.

```Send_Command.py volume decreaseVolume```

This decreases the volume in steps of 5.

```Send_Command.py volume setVolume 50```

This sets the volume to 50%. 

For a documentation on what commands are possible you can take a look at this page:
https://github.com/gmusic-utils/gmusic.js

For an explanation on how the websocket used works read the following page:
https://github.com/MarshallOfSound/Google-Play-Music-Desktop-Player-UNOFFICIAL-/blob/master/docs/PlaybackAPI_WebSocket.md
