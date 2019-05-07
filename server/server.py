#!/usr/bin/env python
from xmlrpc.server import SimpleXMLRPCServer
from endpoints import *
import atexit
import asyncio
import config

def main():
    server = SimpleXMLRPCServer(("localhost", config.PORT))
    print("Listening on port {}".format(config.PORT))

    atexit.register(stop_daemon)
    #  server.register_function(respond, "respond")

    server.register_function(add, "add")

    server.register_function(pause, "pause")
    server.register_function(resume, "resume")
    server.register_function(retrieve, "retrieve")

    server.register_function(remove, "remove")

    server.register_function(info, "info")

    start_daemon()
    server.serve_forever()

if __name__=="__main__":
    main()
