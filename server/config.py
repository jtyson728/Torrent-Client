import os

HOST = "cpp.cs.rutgers.edu"
PORT = 12000
DOWNLOAD_DIR = os.path.join(os.getcwd(), "Downloads");
TORRENT_CACHE = os.path.join(os.getcwd(), ".torrents");

if not os.path.exists(DOWNLOAD_DIR):
    os.mkdir(DOWNLOAD_DIR)

if not os.path.exists(TORRENT_CACHE):
    os.mkdir(TORRENT_CACHE)
