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
 

# acquire .torrent file
# call handler for add
# return unique key of torrent to client
def add(f_names, paths):
	try:
		torrent_paths = []
		for path in paths:
			torrent_path = "{}/{}".format(config.TORRENT_CACHE, path)
			torrent_paths.append(torrent_path)

		run_async(partial(add_torrent, torrent_paths, config.DOWNLOAD_DIR))
		
	except Exception as e:
		print("Exception occurred in add: {}".format(e))
		return e

	torrent_ids = []
	for path in paths:
		torrent_id = secrets.choice(range(1000, 10000))
		torrent_id = str(format(torrent_id, "04"))
		while torrent_id in f_names:
			torrent_id = secrets.choice(range(1000, 10000))
			torrent_id = str(format(torrent_id, "04"))
			torrent_ids.append(torrent_id)
		f_names[torrent_id] = path
	return torrent_ids


def remove(f_names, hash_keys):
	print(hash_keys)
	paths = list(map(
		lambda hash_key: f_names.pop(hash_key), hash_keys))
	print(paths)
	#  import pdb; pdb.set_trace()
	if paths:
		try:
			torrent_paths = []
			for path in paths:
				torrent_path = "{}/{}".format(config.TORRENT_CACHE, path)
				torrent_paths.append(torrent_path)
			run_async(partial(remove_torrent, paths, config.DOWNLOAD_DIR))
		except Exception as e:
			print("Exception occurred: {}".format(e))
			return e
		return list(paths)
	else:
		return FileNotFoundError("Hash key must be invalid")


# pause a download specified by a specific key
def pause(f_names, hash_keys):
	print(hash_keys)
	paths = list(map(
		lambda hash_key: f_names.get(hash_key), hash_keys))
	print(paths)
	#  import pdb; pdb.set_trace()
	if paths:
		try:
			torrent_paths = []
			for path in paths:
				torrent_path = "{}/{}".format(config.TORRENT_CACHE, path)
				torrent_paths.append(torrent_path)
			run_async(partial(pause_torrent, paths, config.DOWNLOAD_DIR))
		except Exception as e:
			print("Exception occurred: {}".format(e))
			return e
		return list(paths)
	else:
		return FileNotFoundError("Hash key must be invalid")


# resume a download specified by a specific key
def resume(f_names, hash_keys):
	print(hash_keys)
	paths = list(map(
		lambda hash_key: f_names.get(hash_key), hash_keys))
	print(paths)
	#  import pdb; pdb.set_trace()
	if paths:
		try:
			torrent_paths = []
			for path in paths:
				torrent_path = "{}/{}".format(config.TORRENT_CACHE, path)
				torrent_paths.append(torrent_path)
		
			run_async(partial(resume_torrent, paths, config.DOWNLOAD_DIR))
		except Exception as e:
			print("Exception occurred: {}".format(e))
			return e
		return list(paths)
	else:
		return FileNotFoundError("Hash key must be invalid")


# retrieve downloaded file on client side
# returns paths (on the server) to directories containing the completed torrents
def retrieve(f_names, hash_keys):
	paths = []
	for key in hash_keys:
		path = f_names.get(key)
		if path:
			paths.append(path.replace(".torrent", "/"))
		else:
			return FileNotFoundError("Hash key {} is invalid".format(key))

	return paths


# displays info on the torrent that you are downloading
def info(f_names, hash_keys):
    for key in hash_keys:
        path = f_names.get(key)
        if path:
            torrent_info = TorrentInfo.from_file(path, download_dir=None)
            content_description = formatters.join_lines(
                    formatters.format_title(torrent_info, True) + formatters.format_content(torrent_info))
            yield content_description
        else:
            yield FileNotFoundError("Hash key {} is invalid".format(key))
