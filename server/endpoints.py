from multiprocessing import Process
from functools import partial
from utils import *
import asyncio
import config
import os
import uuid

from torrent_client.control import ControlManager, ControlClient, ControlServer, DaemonExit, formatters
from torrent_client.models import TorrentInfo, TorrentState

f_names = {}


# call run_daemon create necessary objects and configs
def start_daemon():
    p = Process(target=run_daemon)
    p.start()
    return p


# supposed to exit from server
# stop long-running process
def stop_daemon(p):
    p.terminate()


# acquire .torrent file
# call handler for add
# return unique key of torrent to client
def add(paths):
    global f_names
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
        torrent_id = str(uuid.uuid4())
        while torrent_id in f_names:
            torrent_id = str(uuid.uuid4())

        torrent_ids.append(torrent_id)
        f_names[torrent_id] = path
    return torrent_ids


def remove(hash_keys):
    global f_names
    paths = map(
            lambda hash_key: f_names.pop(hash_key),
            hash_keys)
    if paths:
        try:
            run_async(partial(
                remove_torrent,
                paths))
        except Exception as e:
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
def info(hash_key):
    global f_names
    f_name = f_names[hash_key]
    return None
