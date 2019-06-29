import websockets
import asyncio
import json
import sys, os

path = os.path.dirname(os.path.abspath(sys.argv[0]))+"/"
name = "TP_GMD"
async def connect_API():
	async with websockets.connect("ws://127.0.0.1:5672") as websocket:
		
		announce = {
			"namespace": "connect",
			"method": "connect",
			"arguments": [name]
		}
		
		print(json.dumps(announce))
		await websocket.send(json.dumps(announce))
		
		response = await websocket.recv()
		while "CODE_REQUIRED" not in response:
			response = await websocket.recv()
			if "CODE_REQUIRED" in response:
				break
		print(response)
		code = input("Enter code: ")
					
		connect = {
			"namespace": "connect",
			"method": "connect",
			"arguments": [name, code]
		}
		
		response = websocket.recv()
		
		await websocket.send(json.dumps(connect))
		
		print(connect)
		
		response = await websocket.recv()
		while "CODE_REQUIRED" not in response or name not in response:
			response = await websocket.recv()
			if "CODE_REQUIRED" in response:
				print("Wrong code was entered")
			if "connect" in response:
				file = open(path+"key.json","w+")
				file.write(response)
				file.close() 
				print("Code succesfully retrieved and saved")
				break				
asyncio.get_event_loop().run_until_complete(connect_API())