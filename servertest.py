from xmlrpc.server import SimpleXMLRPCServer

def respond(msg):
	print(msg)
	return("I got the message")

server = SimpleXMLRPCServer(("null.cs.rutgers.edu", 40000))
print("Listening on port 40000...")
server.register_function(respond, "respond")
server.serve_forever()
