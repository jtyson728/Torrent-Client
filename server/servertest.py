#!/usr/bin/env python
import config
from xmlrpc.server import SimpleXMLRPCServer

def respond(msg):
    print(msg)
    return("I got the message")

server = SimpleXMLRPCServer(("null.cs.rutgers.edu", config.PORT))
print("Listening on port {}...".format(config.PORT))
server.register_function(respond, "respond")
server.serve_forever()
