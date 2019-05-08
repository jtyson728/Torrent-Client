#!/usr/bin/env python
import argparse
import asyncio
import config
import sys
import xmlrpc.client
import argh
from contextlib import closing, suppress
from functools import partial
from typing import List

#proxy = xmlrpc.client.ServerProxy("http://{}:{}".format(config.SERVER_URI, config.PORT))

#print(proxy)
#print(proxy.start_daemon())

def add_torrent(paths):
    print("In add")
    hash_key = asyncio.create_task(proxy.add(paths))
    await hash_key
    print("The hash keys for the torrents stored at {} (respectively) are: {}.".format(paths, hash_keys))

async def remove_torrent(hash_keys):
    path = asyncio.create_task(proxy.remove(hash_keys))
    await path
    print("The torrents at paths {} with hash keys {} has been removed.".format(paths, hash_keys))

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    add_parser = subparsers.add_parser("add", help="Add a torrent file to the server")
    add_parser.set_defaults(func=add)
    add_parser.add_parser('filenames', nargs='+', help='Torrent file names')
    #subparser = subparsers.add_argument("remove", help="Remove a torrent on the server", type=str)


    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

