import asyncio
import os
import signal
from contextlib import closing, suppress
from functools import partial
from typing import List

from torrent_client.control import ControlManager, ControlClient, ControlServer, DaemonExit, formatters
from torrent_client.models import TorrentInfo, TorrentState

async def check_daemon_absence():
    try:
        async with ControlClient():
            pass
    except RuntimeError:
        pass
    else:
        raise RuntimeError('The daemon is already running')


def run_daemon():
    with closing(asyncio.get_event_loop()) as loop:
        loop.run_until_complete(check_daemon_absence())

        control = ControlManager()
        loop.run_until_complete(control.start())

        try:
            control.load_state()
        except Exception as err:
            logging.warning('Failed to load program state: %r', err)
        control.invoke_state_dumps()

        stopping = False

        def stop_daemon(server: ControlServer):
            nonlocal stopping
            if stopping:
                return
            stopping = True

            stop_task = asyncio.ensure_future(asyncio.wait([server.stop(), server.control.stop()]))
            stop_task.add_done_callback(lambda fut: loop.stop())

        control_server = ControlServer(control, stop_daemon)
        loop.run_until_complete(control_server.start())

        if os.name == 'posix':
            for sig in (signal.SIGINT, signal.SIGTERM):
                loop.add_signal_handler(sig, partial(stop_daemon, control_server))

        loop.run_forever()


async def add_torrent(paths, download_dir):
    torrents = map(
            lambda path: TorrentInfo.from_file(path, download_dir),
            paths)
    async with ControlClient() as client:
        for info in torrents:
            await client.execute(
                    partial(
                        ControlManager.add,
                        torrent_info=info))


async def remove_torrent(paths):
    torrents = map(
            lambda path: TorrentInfo.from_file(path, download_dir),
            paths)
    
    async with ControlClient() as client:
        for info in torrents:
            await client.execute(
                    partial(
                        ControlManager.remove,
                        torrent_info=info))

