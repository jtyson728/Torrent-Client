#!/usr/bin/env python
from functools import partial
import argparse
import asyncio 
import config
import sys
import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://{}:{}".format(config.SERVER_URI, config.PORT))

print(proxy)
#  print(proxy.start_daemon())

async def add(args):
    print("Going inside add")
    hash_key = asyncio.create_task(proxy.add(args.filenames))
    await hash_key
    print("The hash keys for the torrents stored at {} (respectively) are: {}.".format(paths, hash_keys))

async def remove(args):
    paths = asyncio.create_task(proxy.remove(args.hash_keys))
    await paths
    print("The torrents at paths {} with hash keys {} has been removed.".format(paths, args.hash_keys))

def run(coro, args):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro(args))

def main():
    parser = argparse.ArgumentParser(description="A client for the torrent RPC server (CLI)")

    subparsers = parser.add_subparsers(
            description="Specify an action before --help to show parameters for it",
            metavar="ACTION",
            dest="action")

    # subparser for add
    subparser = subparsers.add_parser(
            "add",
            help="Add a torrent to the server")

    subparser.add_argument(
            "filenames",
            nargs="+",
            help="Torrent file names")
    subparser.set_defaults(func=partial(run, add))

    subparser = subparsers.add_parser(
            "remove",
            help="Remove a torrent from the server with hash key")

    subparser.add_argument(
            "hash_keys",
            nargs="+",
            help="Hash keys of torrents to remove")
    subparser.set_defaults(func=partial(run, remove))

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
