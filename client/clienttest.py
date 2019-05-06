#!/usr/bin/env python
import xmlrpc.client
import sys
import config

with xmlrpc.client.ServerProxy("http://localhost:{}".format(config.PORT)) as proxy: 
    print(proxy)

print(proxy.start_daemon())
