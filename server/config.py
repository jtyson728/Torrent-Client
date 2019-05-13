import os

HOST = "python.cs.rutgers.edu"
PORT = 12000
DOWNLOAD_DIR = os.path.join(os.getcwd(), "Downloads");
TORRENT_CACHE = os.path.join(os.getcwd(), ".torrents");
KEYS_PATH = os.path.join(os.getcwd(), "hash_keys.json")

if not os.path.exists(DOWNLOAD_DIR):
    os.mkdir(DOWNLOAD_DIR)

if not os.path.exists(TORRENT_CACHE):
    os.mkdir(TORRENT_CACHE)
