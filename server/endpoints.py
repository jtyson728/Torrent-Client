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
		torrent_paths = []
		for f_name in files:
			torrent_path = "{}/{}".format(config.TORRENT_CACHE, f_name)
			torrent_paths.append(torrent_path)

		run_async(partial(add_torrent, torrent_paths, config.DOWNLOAD_DIR))
	except Exception as e:
		print("Exception occurred in add: {}".format(e))
		return e

	torrent_ids = []
	for f_name in files:
		torrent_id = str(format(secrets.choice(range(1000, 10000)), "04"))
		while torrent_id in f_names:
			torrent_id = str(format(secrets.choice(range(1000, 10000)), "04"))
			torrent_ids.append(torrent_id)

        torrent_dir = os.path.join(os.getcwd(), config.DOWNLOAD_DIR)
        torrent-dir = os.path.join(torrent_dir, f_name.replace(".torrent", ""))

		f_names[torrent_id] = [f_name, torrent_dir]
        torrent_ids.append(torrent_id)
	return torrent_ids


def remove(f_names, hash_keys):
	print(hash_keys)
    path_lists j= list(map(
                lambda hash_key: f_names.pop(hash_key),
                hash_keys))
	#  import pdb; pdb.set_trace()
	if path_lists:
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
