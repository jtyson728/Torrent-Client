from utorrentapi import UTorrentAPI
import xmlrpc.client
try:
        proxy = xmlrpc.client.ServerProxy("http://factory.cs.rutgers.edu:8000/")
finally:
        print("3 is even: %s" % str(proxy.is_even(3)))
        print("100 is even: %s" % str(proxy.is_even(100))


apiclient = UTorrentAPI('http://127.0.0.1:35653/gui', 'admin', 'laky123')

if apiclient is not None:
    torrents = apiclient.get_list()

    index = 0
    for torrent in torrents['torrents']:
        name = '%i - %s' % (index, torrent[2])
        index+=1
        print(name)
    # apiclient.get_files(torrent[0])
    # apiclient.recheck(torrent[0])
    # apiclient.set_priority(torrent[0], 1, 1)
