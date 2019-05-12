#!/usr/bin/env python
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from functools import partial
from endpoints import *
from subprocess import call
import zlib
import xmlrpc.client
import atexit
import asyncio
import config
import urllib




class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ("/RPC2",)

def send_file():
	with open("test.txt", "rb") as handle:
		return xmlrpc.client.Binary(handle.read())

def push(f_name, binaryData):
	tfPath = "{}/{}".format(config.TORRENT_CACHE, f_name)
	with open(tfPath, "wb") as tFile:
		tFile.write(binaryData.data);
		return True
		
		
def main():
	
	# make download dir if it doesn't exist already
	if not os.path.exists(config.DOWNLOAD_DIR):
		os.mkdir(config.DOWNLOAD_DIR)
	if not os.path.exists(config.TORRENT_CACHE):
		os.mkdir(config.TORRENT_CACHE)
	

	proc, file_table = start_server()
	atexit.register(destroy_server, proc, file_table)

	server = SimpleXMLRPCServer((config.HOST, config.PORT))

	
	print("Listening on port {}".format(config.PORT))

	server.register_function(
		partial(add, file_table), "add")

	server.register_function(
		partial(pause, file_table), "pause")

	server.register_function(
		partial(resume, file_table), "resume")

	server.register_function(
		partial(retrieve, file_table), "retrieve")

	server.register_function(
		partial(remove, file_table), "remove")

	server.register_function(
		partial(info, file_table), "info")	
	
	server.register_function(push, "push")
	
	server.register_function(send_file, 'pull')
	
	server.serve_forever()

if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Server Shutting Down...")
		sys.exit(0)
