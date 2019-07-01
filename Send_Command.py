from websocket import create_connection
import asyncio
import json
import sys, os

#Set the path and name used to communicate with the desktop software.
path = os.path.dirname(sys.argv[0])  +"\\"
name = "GPMD"

#Used to initiate a connection through websocket.
ws = create_connection("ws://127.0.0.1:5672")

#Function responsible for writing a authentication token to key.json.
def getToken_API(): 
        announce = {
                "namespace": "connect",
                "method": "connect",
                "arguments": [name]
        }
        ws.send(json.dumps(announce))

        response = ws.recv()

        #Wait till we get the confirmation from the server that it succesfully received our message.
        while "CODE_REQUIRED" not in response:
                response = ws.recv()
                if "CODE_REQUIRED" in response:
                        break

        #Ask for the user for the code that is given from the desktop application.
        code = input("Enter code: ")
                                
        connect = {
                "namespace": "connect",
                "method": "connect",
                "arguments": [name, code]
        }

        ws.send(json.dumps(connect))

        #Get the response and wait for the reply that either tells us the proper code was used or not.
        response = ws.recv()
        while "CODE_REQUIRED" not in response or name not in response:
                response = ws.recv()
                if "CODE_REQUIRED" in response:
                        print("Wrong code was entered.")
                        ws.close()
                        exit()
                if "connect" in response:
                        #Code was correct, now we need to write it out to a new file.
                        file = open(path+"key.json","w+")
                        file.write(response)
                        file.close()
                        ws.close()
                        print("Code succesfully retrieved and saved.")
                        print("Rerun the script to execute a command.")
                        exit()

#The Function to actually send out commands to the desktop software.
def sendCommand():
        #First we need to send the actual key from the key.json file to authenticate ourselves.
        announce = {
                "namespace": "connect",
                "method": "connect",
                "arguments": ["TP_GMD", key]
        }

        ws.send(json.dumps(announce))

        #Check if we have a command without an argument or with an argument based on the amount of commandline parameters given.
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

#Check if the proper format was used to call the script.
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

#Checking if the key.json file is present.      
if not os.path.isfile(path+"key.json"):
        print("Key file not present. Make sure you configured the key with \"Send_Command.py configure\"")
        exit()

#If this file is present extract the key itself from the json.
with open(path+"key.json", "r") as key_json:
        key_dict = json.load(key_json)
        key = key_dict["payload"]

sendCommand()

