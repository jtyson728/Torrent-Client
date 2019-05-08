#!/usr/bin/env python
from xmlrpc.server import SimpleXMLRPCServer
from functools import partial
from endpoints import *
import atexit
import asyncio
import config

def main():
    # make download dir if it doesn't exist already
    if not os.path.exists(config.DOWNLOAD_DIR):
        os.mkdir(config.DOWNLOAD_DIR)

    server = SimpleXMLRPCServer(("localhost", config.PORT))
    print("Listening on port {}".format(config.PORT))

    server.register_function(add, "add")

    server.register_function(pause, "pause")
    server.register_function(resume, "resume")
    server.register_function(retrieve, "retrieve")

    server.register_function(remove, "remove")
    server.register_function(info, "info")

    proc = start_daemon()
    atexit.register(partial(stop_daemon, proc))
    server.serve_forever()

if __name__=="__main__":
    main()
