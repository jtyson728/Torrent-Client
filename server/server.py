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


# call run_daemon create necessary objects and configs
def start_server():
    p = Process(target=run_daemon)
    p.start()

    keys_path = os.path.join(os.getcwd(), "hash_keys.json")

    if os.path.exists(keys_path):
        with open(keys_path) as keys_file:
            return (p, json.load(keys_file))
    else:
        return (p, {})


# supposed to exit from server
# stop long-running process
def destroy_server(p, f_names):
    try:
        p.terminate()
    except:
        print("Process already exited.")

    keys_path = os.path.join(
            os.getcwd(),
            "hash_keys.json")

    if f_names:
        if os.path.exists(keys_path):
            os.remove(keys_path)
            
        with open(keys_path, "w+") as keys_file:
            json.dump(f_names, keys_file)


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
	
	server.register_function(receive_file, "receive_file")
	
	server.serve_forever()

if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Server Shutting Down...")
		sys.exit(0)
