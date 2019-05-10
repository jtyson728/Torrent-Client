#!/usr/bin/env python
from functools import partial
import argparse
import asyncio 
import config
import sys
import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://{}:{}/".format(config.SERVER_URI, config.PORT))

#  print(proxy)
#  print(proxy.start_daemon())

def add(args):
    hash_keys = proxy.add(args.filenames)
    if isinstance(hash_keys, Exception):
        print("Exception occurred: {}".format(hash_keys))
    else:
        print("The hash keys for the torrents stored at {} (respectively) are: {}.".format(args.filenames, hash_keys))


def remove(args):
    print(args)
    paths = proxy.remove(args.hash_keys)
    if isinstance(paths, Exception):
        print("Exception occurred: {}".format(paths))
    else:
        print("The torrents at paths {} with hash keys {} has been removed.".format(paths, args.hash_keys))

def pause(args):
    print(args)
    paths = proxy.pause(args.hash_keys)
    if isinstance(paths, Exception):
        print("Exception occurred: {}".format(paths))
    else:
        print("The torrents at paths {} with hash keys {} has been removed.".format(paths, args.hash_keys))

def resume(args):
    print(args)
    paths = proxy.resume(args.hash_keys)
    if isinstance(paths, Exception):
        print("Exception occurred: {}".format(paths))
    else:
        print("The torrents at paths {} with hash keys {} has been removed.".format(paths, args.hash_keys))




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

    subparser.set_defaults(func=add)

    subparser = subparsers.add_parser(
            "remove",
            help="Remove a torrent from the server with hash key")

    subparser.add_argument(
            "hash_keys",
            nargs="+",
            help="Hash keys of torrents to remove")

    subparser.set_defaults(func=remove)

	subparser = subparsers.add_parser(
			"pause",
			help="Pause a torrent that is currently downloading on the server with hash key")

	subparser.add_argument(
			"hask_keys",
			nargs="+",
			help="Hash keys of torrents to remove")
	subparser.set_defaults(func=pause)

subparser = subparsers.add_parser(
			"resume",
			help="Resume a torrent that is currently paused on the server with hash key")

	subparser.add_argument(
			"hask_keys",
			nargs="+",
			help="Hash keys of torrents to remove")
	subparser.set_defaults(func=pause)


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
