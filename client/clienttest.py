#!/usr/bin/env python
import argparse
import asyncio 
import config
import sys
import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://{}:{}".format(config.SERVER_URI, config.PORT))

print(proxy)
print(proxy.start_daemon())

async def add_torrent(paths):
    hash_key = asyncio.create_task(proxy.add(paths))
    await hash_key
    print("The hash keys for the torrents stored at {} (respectively) are: {}.".format(paths, hash_keys))

async def remove_torrent(hash_keys):
    path = asyncio.create_task(proxy.remove(hash_keys))
    await path
    print("The torrents at paths {} with hash keys {} has been removed.".format(paths, hash_keys))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "add",
            help="Add a torrent file to the server",
            type=str)

    parser.add_argument(
            "remove",
            help="Remove a torrent on the server",
            type=str)


    args = parser.parse_args()
    if args.add:
        # execute add functionality
    elif args.remove:
        # execute remove functionality

    return 0

if __name__=="__main__":
    main()
