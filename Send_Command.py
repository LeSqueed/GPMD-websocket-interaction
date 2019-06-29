import os.path
import websockets
import json
import asyncio
import sys, os

namespace=sys.argv[1]
command=sys.argv[2]
if len(sys.argv) > 3:
	argument=sys.argv[3]
	print(argument)
path = os.path.dirname(os.path.abspath(sys.argv[0]))+"/"
name = "TP_GMD"

print(path)
if not os.path.isfile(path+"key.json"):
    print("There is no key file, please run Get_Token.py to generate a key.")
else:
	with open(path+"key.json", "r") as key_json:
		key_dict = json.load(key_json)
		key = key_dict["payload"]
	async def connect_API():
		async with websockets.connect("ws://127.0.0.1:5672") as websocket:
			
			announce = {
				"namespace": "connect",
				"method": "connect",
				"arguments": ["TP_GMD", key]
			}

			await websocket.send(json.dumps(announce))
			
			if len(sys.argv) < 4:
				wsCommand = {
					"namespace": namespace,
					"method": command
				}
			else:
				wsCommand = {
					"namespace": namespace,
					"method": command,
					"arguments": "[1000]",
					"requestID": 1
				}
			
			print("Send following request: "+json.dumps(wsCommand))
			await websocket.send(json.dumps(wsCommand))
	asyncio.get_event_loop().run_until_complete(connect_API())