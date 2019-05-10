from multiprocessing import Process
from functools import partial
from utils import *
import asyncio
import config
import os
import json
import secrets
import shutil
import uuid

from torrent_client.control import ControlManager, ControlClient, ControlServer, DaemonExit, formatters
from torrent_client.models import TorrentInfo, TorrentState


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

    keys_path = os.path.join(os.getcwd(), "hash_keys.json")
    if f_names:
        if os.path.exists(keys_path):
            os.remove(keys_path)
            
        with open(keys_path, "w+") as keys_file:
            json.dump(f_names, keys_file)
 
    shutil.rmtree(config.DOWNLOAD_DIR) 


# acquire .torrent file
# call handler for add
# return unique key of torrent to client
def add(f_names, paths):
    try:
        run_async(partial(
            add_torrent,
            paths,
            config.DOWNLOAD_DIR))
    except Exception as e:
        print("Exception occurred: {}".format(e))
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
                lambda hash_key: f_names.pop(hash_key),
                hash_keys))
    print(paths)
    #  import pdb; pdb.set_trace()
    if paths:
        try:
            run_async(partial(
                remove_torrent,
                paths,
                config.DOWNLOAD_DIR))
        except Exception as e:
            print("Exception occurred: {}".format(e))
            return e
        return list(paths)
    else:
        return FileNotFoundError("Hash key must be invalid")


# pause a download specified by a specific key
def pause():
    return None


# resume a download specified by a specific key
def resume():
    return None


# retrieve downloaded file on client side
def retrieve():
    return None


# displays info on the torrent that you are downloading
def info(f_names, hash_key):
    f_name = f_names[hash_key]
    return None
