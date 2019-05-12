#!/usr/bin/env python
from functools import partial
from paramiko import SSHClient
from utils import *
from scp import SCPClient
import argparse
import asyncio 
import config
import os
import shutil
import sys
import xmlrpc.client
import time


proxy = None

def python_logo():
	pass

def make_subparser(parser, name, callback, arg_name, subparsers, nargs="+", help_message=""): 
	subparser = subparsers.add_parser(name, help=help_message)

	subparser.add_argument(arg_name, nargs=nargs, help="")

	subparser.set_defaults(func=callback)


def add(args):
	if config.SERVER_URI.lower() != "localhost":   
		with SCPClient(ssh.get_transport()) as scp:
			for f_name in args.filenames:
				base = os.path.basename(f_name)
				scp.put(f_name, os.path.join(config.TORRENT_DIR, base))
        
	hash_keys = proxy.add(args.filenames)
	if isinstance(hash_keys, Exception):
		print("Exception occurred: {}".format(hash_keys))
	else:
		print("The hash keys for the torrents stored at {} (respectively) are: {}.".format(args.filenames, hash_keys))


def remove(args):
	paths = proxy.remove(args.hash_keys)
	if isinstance(paths, Exception):
		print("Exception occurred: {}".format(paths))
	else:
		print("The torrents at paths {} with hash keys {} has been removed.".format(paths, args.hash_keys))


def pause(args):
	paths = proxy.pause(args.hash_keys)
	if isinstance(paths, Exception):
		print("Exception occurred: {}".format(paths))
	else:
		print("The torrents at paths {} with hash keys {} has been removed.".format(paths, args.hash_keys))


def resume(args):
	paths = proxy.resume(args.hash_keys)
	if isinstance(paths, Exception):
		print("Exception occurred: {}".format(paths))
	else:
		print("The torrents at paths {} with hash keys {} has been removed.".format(paths, args.hash_keys))


def info(args):
	for info in proxy.add(args.hash_keys):
		if isinstance(info, str):
			print(info)
		else:
			print("Exception occurred: {}".format(info))
			sys.exit(-1)


def retrieve(args):
	is_remote = config.SERVER_URI != "localhost"
	if is_remote:
        
		for path in proxy.retrieve(args.hash_keys):
			if is_remote:
				# scp -r each of the directories
				scp.get(path, recursive=True)
			else:
				# normal copy each directory tree
				shutil.copytree(path, os.getcwd())
 
def main():
	#transport = ProxyInterface()
	try:
		proxy = xmlrpc.client.ServerProxy("http://{}:{}/".format(config.SERVER_URI, config.SERVER_PORT))
		time.sleep(1)
		print(proxy)
		
	except xmlrpc.client.Fault as err:
		print("a Fault error ocurred.")
		print("Fault code: %d", err.faultCode)
		print("Fault Message: %s", err.faultString)
	
	else:
		with open("lol.txt", "wb") as handle:
			handle.write(proxy.python_logo().data)
		parser = argparse.ArgumentParser(description="A client for the torrent RPC server (CLI)")

		subparsers = parser.add_subparsers(
			description="Specify an action before --help to show parameters for it",
			metavar="ACTION",
			dest="action")

		# subparser for add
		make_subparser(parser, name="add", callback=add, arg_name="filenames", subparsers=subparsers)

		make_subparser(parser, name="remove", callback=remove, arg_name="hash_keys", subparsers=subparsers)

		make_subparser(parser, name="pause", callback=pause, arg_name="hash_keys", subparsers=subparsers)

		make_subparser(parser, name="resume", callback=resume, arg_name="hash_keys", subparsers=subparsers)

		make_subparser(parser, name="info", callback=info, arg_name="hash_keys", subparsers=subparsers)

		make_subparser(parser, name="retrieve", callback=retrieve, arg_name="hash_keys", subparsers=subparsers)
	
		make_subparser(parser, name="pull", callback=retrieve, arg_name="hash_keys", subparsers=subparsers)
		
		arguments = parser.parse_args()

		try:
			# try to run appropriate function
			arguments.func(arguments)
		except Exception as e:
			print("Exception occurred: {}".format(e))
			return -1

		return 0



if __name__=="__main__":
    main()
