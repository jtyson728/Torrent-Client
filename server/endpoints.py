from multiprocessing import Process
from functools import partial
import asyncio
import os
import uuid
import utils

from torrent_client.control import ControlManager, ControlClient, ControlServer, DaemonExit, formatters
from torrent_client.models import TorrentInfo, TorrentState

p = None
f_names = {}


#  def respond(msg):
    #  print(msg)
    #  return("I got the message")


# call run_daemon create necessary objects and configs
def start_daemon():
    global p

    p = Process(target=utils.run_daemon)
    p.start()


# supposed to exit from server
# stop long-running process
def stop_daemon():
    global p
    p.terminate()


# acquire .torrent file
# call handler for add
# return unique key of torrent to client
async def add(paths):
    global f_names
    try:
        await add_torrent(
                paths,
                config.DOWNLOAD_DIR)
    except Exception as e:
        return e

    torrent_id = ""
    while torrent_id in f_names:
        torrent_id = str(uuid.uuid4())

    f_names[torrent_id] = path

    return torrent_id 


async def remove(hash_keys):
    global f_names
    paths = map(
            f_names.pop(hash_key),
            hash_keys)
    if paths:
        try:
            await remove_torrent(paths)
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
