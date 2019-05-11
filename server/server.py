#!/usr/bin/env python
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from functools import partial
from endpoints import *
import xmlrpc.client
import atexit
import asyncio
import config


class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ("/RPC2",)

def add():
	print("Got an add request.");

def python_logo():
	with open("test.txt", "rb") as handle:
		return xmlrpc.client.Binary(handle.read())


def main():
	
	# make download dir if it doesn't exist already
	if not os.path.exists(config.DOWNLOAD_DIR):
		os.mkdir(config.DOWNLOAD_DIR)
	
	

	proc, file_table = start_server()
	atexit.register(destroy_server, proc, file_table)

	server = SimpleXMLRPCServer((config.HOST, config.PORT))

	
	print("Listening on port {}".format(config.PORT))
	
	server.register_function(python_logo, 'python_logo')
	server.register_function(fetch_torrent)
	server.serve_forever()

if __name__=="__main__":
    main()
