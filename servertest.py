from xmlrpc.server import SimpleXMLRPCServer

def is_even(n):
    return n % 2 == 0

server = SimpleXMLRPCServer(("factory.cs.rutgers.edu", 8000))
print("Listening on port 8000...")
server.register_function(is_even, "is_even")
server.serve_forever()
