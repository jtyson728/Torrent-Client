import xmlrpc.client

with xmlrpc.client.ServerProxy("http://null.cs.rutgers.edu:40000/") as proxy:
    print(proxy)
    while 1:
        cmd = input("Next command \n")
    if "respond" in cmd:
        msg = cmd.replace("respond ", "")
        print(proxy.respond(msg))
