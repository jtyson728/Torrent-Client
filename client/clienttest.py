#!/usr/bin/env python
import xmlrpc.client
import sys
import config
import argparse

proxy = xmlrpc.client.ServerProxy("http://localhost:{}".format(config.PORT))

print(proxy)
print(proxy.start_daemon())

async def add_torrent(path):
    hash_key = asyncio.create_task(proxy.add(path))
    await hash_key
    print("The hash key for the torrent stored at {} is: {}.".format(path, hash_key))

async def remove_torrent(hash_key):
    path = asyncio.create_task(proxy.remove(hash_key))
    await path
    print("The torrent at path {} with hash key {} has been removed.".format(path, hash_key))

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
