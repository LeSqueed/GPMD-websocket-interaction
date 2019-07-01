from websocket import create_connection
import asyncio
import json
import sys, os

path = os.path.dirname(sys.argv[0])  +"\\"
name = "GPMD"

ws = create_connection("ws://127.0.0.1:5672")

def getToken_API(): 
        announce = {
                "namespace": "connect",
                "method": "connect",
                "arguments": [name]
        }
        ws.send(json.dumps(announce))

        response = ws.recv()
        while "CODE_REQUIRED" not in response:
                response = ws.recv()
                if "CODE_REQUIRED" in response:
                        break
                
        code = input("Enter code: ")
                                
        connect = {
                "namespace": "connect",
                "method": "connect",
                "arguments": [name, code]
        }

        ws.send(json.dumps(connect))
        
        response = ws.recv()
        while "CODE_REQUIRED" not in response or name not in response:
                response = ws.recv()
                if "CODE_REQUIRED" in response:
                        print("Wrong code was entered.")
                        ws.close()
                        exit()
                if "connect" in response:
                        file = open(path+"key.json","w+")
                        file.write(response)
                        file.close()
                        ws.close()
                        print("Code succesfully retrieved and saved.")
                        print("Rerun the script to execute a command.")
                        exit()
                        
if len(sys.argv) < 2:
        print("Not enough parameters given")
        exit()
elif len(sys.argv) == 2 and sys.argv[1] == "configure":
        getToken_API()
elif len(sys.argv) == 2 and sys.argv[1] != "configure":
        print("Invalid parameters given.")
        exit()
elif len(sys.argv) > 4:
        print("Too many parameters given.")
        exit()
else:
        namespace=sys.argv[1]
        command=sys.argv[2]
        if len(sys.argv) > 3:
                argument=sys.argv[3]

        
if not os.path.isfile(path+"key.json"):
        print("Key file not present. Make sure you configured the key with \"Send_Command.py configure\"")
        exit()

with open(path+"key.json", "r") as key_json:
        key_dict = json.load(key_json)
        key = key_dict["payload"]

def sendCommand():
        announce = {
                "namespace": "connect",
                "method": "connect",
                "arguments": ["TP_GMD", key]
        }

        ws.send(json.dumps(announce))

        if len(sys.argv) < 4:
                wsCommand = {
                        "namespace": namespace,
                        "method": command
                }
        else:
                wsCommand = {
                        "namespace": namespace,
                        "method": command,
                        "arguments": "["+argument+"]"
                }
        ws.send(json.dumps(wsCommand))
        print("Send following request: "+json.dumps(wsCommand))
        ws.close()
sendCommand()

