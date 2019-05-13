#!/usr/bin/env python
from functools import partial
# from paramiko import SSHClient
# from utils import *
# from scp import SCPClient
import argparse
import asyncio 
import config
import os
import shutil
import sys
import xmlrpc.client
import time

proxy = None

try:
    proxy = xmlrpc.client.ServerProxy("http://{}:{}/".format(config.SERVER_URI, config.SERVER_PORT))
    time.sleep(3)
		
except xmlrpc.client.Fault as err:
    print("Connection fault occurred.")
    print("Fault code: %d", err.faultCode)
    print("Fault Message: %s", err.faultString)
    sys.exit(-1)


def send_file(path):
    with open(path, "rb") as handle:
        binary_data = xmlrpc.client.Binary(handle.read())
    proxy.receive_file(os.path.basename(path), binary_data)


def make_subparser(parser, name, callback, subparsers, arg_name=None, nargs="+", help_message=""): 
    subparser = subparsers.add_parser(name, help=help_message)
    if arg_name:
        subparser.add_argument(arg_name, nargs=nargs, help="")
    subparser.set_defaults(func=callback)


def add(args):
    for f_path in args.filenames:
        send_file(f_path)
    hash_keys = proxy.add([os.path.basename(f_path) for f_path in args.filenames])
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
        print("The torrents at paths {} with hash keys {} have been paused.".format(paths, args.hash_keys))


def resume(args):
    paths = proxy.resume(args.hash_keys)
    if isinstance(paths, Exception):
        print("Exception occurred: {}".format(paths))
    else:
        print("The torrents at paths {} with hash keys {} has been resumed.".format(paths, args.hash_keys))


def info(args):
    info = proxy.info()
    if isinstance(info, str):
        print(info)
    else:
        print("Exception occurred: {}".format(info))
        sys.exit(-1)


def retrieve(args):
    server_paths = proxy.retrieve(args.hash_keys)
    print("Paths on the server side are: {}. Use SCP (or similar) to retrieve them.".format(server_paths))


def main():
    parser = argparse.ArgumentParser(description="A client for the torrent RPC server (CLI)")

    subparsers = parser.add_subparsers(
            description="Specify an action before --help to show parameters for it",
            metavar="ACTION",
            dest="action")

    # subparser for add
    make_subparser(
            parser,
            name="add",
            callback=add,
            arg_name="filenames",
            subparsers=subparsers)

    make_subparser(
            parser,
            name="remove",
            callback=remove,
            arg_name="hash_keys",
            subparsers=subparsers)

    make_subparser(
            parser,
            name="pause",
            callback=pause,
            arg_name="hash_keys",
            subparsers=subparsers)

    make_subparser(
            parser,
            name="resume",
            callback=resume,
            arg_name="hash_keys",
            subparsers=subparsers)

    make_subparser(
            parser,
            name="info",
            callback=info,
            subparsers=subparsers)

    make_subparser(
            parser,
            name="retrieve",
            callback=retrieve,
            arg_name="hash_keys",
            subparsers=subparsers)
    
    # make_subparser(parser, name="push", callback=push, arg_name="filenames", subparsers=subparsers)
            
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
