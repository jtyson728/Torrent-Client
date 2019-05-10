#!/usr/bin/env python
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from functools import partial
from endpoints import *
import atexit
import asyncio
import config


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)

def main():
    # make download dir if it doesn't exist already
    if not os.path.exists(config.DOWNLOAD_DIR):
        os.mkdir(config.DOWNLOAD_DIR)

    proc, file_table = start_server()
    atexit.register(destroy_server, proc, file_table)

    server = SimpleXMLRPCServer((config.HOST, config.PORT),
            requestHandler=RequestHandler)

    print("Listening on port {}".format(config.PORT))

    server.register_function(
            partial(add, file_table),
            "add")

    server.register_function(
            partial(pause, file_table),
            "pause")
    server.register_function(
            partial(resume, file_table),
            "resume")
    server.register_function(
            partial(retrieve, file_table),
            "retrieve")

    server.register_function(
            partial(remove, file_table),
            "remove")
    server.register_function(
            partial(info, file_table),
            "info")
        
    server.serve_forever()

if __name__=="__main__":
    main()
