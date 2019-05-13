from multiprocessing import Process
from functools import partial
from utils import *
import asyncio
import config
import os
import json
import re
import secrets
import string
import uuid


def receive_file(f_name, binaryData):
	tfPath = "{}/{}".format(config.TORRENT_CACHE, f_name)
	with open(tfPath, "wb") as tFile:
		tFile.write(binaryData.data);
		return True
	

# acquire .torrent file
# call handler for add
# return unique key of torrent to client
def add(f_names, files):
	try:
		run_async(partial(
			add_torrent,
			map(partial(os.path.join, config.TORRENT_CACHE), files),
			config.DOWNLOAD_DIR))
	except Exception as e:
		print("Exception occurred in add: {}".format(e))
		return e

	torrent_ids = []
	for f_name in files:
		torrent_id = str(format(secrets.choice(range(1000, 10000)), "04"))
		while torrent_id in f_names:
			torrent_id = str(format(secrets.choice(range(1000, 10000)), "04"))
		f_names[torrent_id] = f_name
		torrent_ids.append(torrent_id)
	return torrent_ids


def remove(f_names, hash_keys):
	paths = list(map(
		lambda hash_key: os.path.join(config.TORRENT_CACHE, f_names.pop(hash_key)) if f_names.get(hash_key) else None,
		hash_keys))
	#  import pdb; pdb.set_trace()
	if paths and None not in paths:
		try:
			run_async(partial(remove_torrent, paths, config.DOWNLOAD_DIR))
			return list(paths)
		except Exception as e:
			print("Exception occurred: {}".format(e))
			return e
	else:
		return FileNotFoundError("Hash key must be invalid")


# pause a download specified by a specific key
def pause(f_names, hash_keys):
	paths = list(map(
		partial(os.path.join, config.TORRENT_CACHE),
		map(
			f_names.get,
			hash_keys)))
	if paths:
		try:
			run_async(partial(
				pause_torrent,
				paths,
				config.DOWNLOAD_DIR))
			return list(paths)
		except Exception as e:
			print("Exception occurred: {}".format(e))
			return e
	else:
		return FileNotFoundError("Hash key must be invalid")


# resume a download specified by a specific key
def resume(f_names, hash_keys):
	paths = list(map(
		lambda f_name: os.path.join(config.TORRENT_CACHE, f_name) if f_name else None,
		map(
			f_names.get,
			hash_keys)))

	if paths:
		try:
			run_async(partial(
				resume_torrent,
				paths,
				config.DOWNLOAD_DIR))
			return list(paths)
		except Exception as e:
			print("Exception occurred: {}".format(e))
			return e
	else:
		return FileNotFoundError("Hash key must be invalid")


# retrieve downloaded file on client side
# returns paths (on the server) to directories containing the completed torrents
def retrieve(f_names, hash_keys):
	paths = []
	for key in hash_keys:
		f_name = f_names.get(key)
		if f_name:
			path = os.path.join(config.TORRENT_CACHE, f_name)
			paths.append(path)
		else:
			return FileNotFoundError("Hash key {} is invalid".format(key))

	return paths


# displays info on the torrent that you are downloading
def info(f_names):
    return run_async(status_handler) 

