#!/usr/bin/env python
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from functools import partial
from endpoints import *
import atexit
import asyncio
import config


def main():
    # make download dir if it doesn't exist already
    if not os.path.exists(config.DOWNLOAD_DIR):
        os.mkdir(config.DOWNLOAD_DIR)

    proc = start_daemon()
    atexit.register(partial(stop_daemon, proc))

    server = SimpleXMLRPCServer(("localhost", config.PORT),
            requestHandler=SimpleXMLRPCRequestHandler)

    print("Listening on port {}".format(config.PORT))

    f_names = dict()

    server.register_function(
            partial(add, f_names),
            "add")

    server.register_function(
            partial(pause, f_names),
            "pause")
    server.register_function(
            partial(resume, f_names),
            "resume")
    server.register_function(
            partial(retrieve, f_names),
            "retrieve")

    server.register_function(
            partial(remove, f_names),
            "remove")
    server.register_function(
            partial(info, f_names),
            "info")

    server.serve_forever()

if __name__=="__main__":
    main()
