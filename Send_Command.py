from websocket import create_connection
import asyncio
import json
import sys, os
import configparser

#Set the path and name used to communicate with the desktop software.
config = configparser.ConfigParser()
config.read("config.ini")
configServer = config["SERVER"]
key = configServer["key"]
path = os.path.dirname(sys.argv[0])  +"\\"
name = "GPMD"

def connect():
    ws = create_connection("ws://"+configServer["host"]+":"+configServer["port"])
    
def configure():
    Host = input("WS IP default(127.0.0.1): ") or "127.0.0.1"
    Port = input("WS Port (default 5672): ") or "5672"
    
    configServer["host"] = Host
    configServer["port"] = Port
    
    with open("config.ini", "w") as configfile:
        config.write(configfile)

#Function responsible for writing a authentication token to config.ini    
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
    while True:
        response = ws.recv()
        if "CODE_REQUIRED" in response:
                print("Wrong code was entered.")
                ws.close()
                exit()
        if "connect" in response:
                #Code was correct, now we need to write out our config file.
                respDict = json.loads(response)
                configServer["key"] = respDict["payload"]
                with open("config.ini", "w") as configfile:
                    config.write(configfile)
                print("Config saved.")
                ws.close()
                exit()

#The Function to actually send out commands to the desktop software.
def sendCommand():
    #First we need to send the key to authenticate ourselves.
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
            ws.send(json.dumps(wsCommand,ensure_ascii=True))
                
    else:
            wsCommand = {
                    "namespace": namespace,
                    "method": command,
                    "arguments": argument
            }
            ws.send(json.dumps(wsCommand,ensure_ascii=True).replace('"'+argument+'"',argument))
            print(json.dumps(wsCommand,ensure_ascii=True).replace('"'+argument+'"',argument))
            
    ws.close()

#Check if the proper format was used to call the script.
if len(sys.argv) < 2:
        print("Not enough parameters given")
        exit()
elif len(sys.argv) == 2 and sys.argv[1] == "configure":
        configure()
        ws = create_connection("ws://"+configServer["host"]+":"+configServer["port"])
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
                argument="[{0}]".format(sys.argv[3])

ws = create_connection("ws://"+configServer["host"]+":"+configServer["port"])
sendCommand()

