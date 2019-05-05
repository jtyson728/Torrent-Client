#!/usr/bin/env python
import config
from xmlrpc.server import SimpleXMLRPCServer

def respond(msg):
    print(msg)
    return("I got the message")

def start_daemon():
    return("run_daemon create necessary objects and configs")

def stop_daemon():
    print("supposed to exit from server, halt long-running process")

def add_tor():
    print("acquire .torrent file, call handler for add, return unique key of torrent to client")

def pause():
    print("pause a download specified by a specific key")

def resume():
    print("resume a download specified by a specific key")

def retrieve():
    print("retrieve downloaded file on client side")

def info():
    print("displays info on the torrent that you are downloading")

server = SimpleXMLRPCServer(("null.cs.rutgers.edu", 8000))
print("Listening on port 8000")
server.register_function(respond, "respond")
server.register_function(start_daemon, "start_daemon")
server.register_function(stop_daemon, "stop_daemon")
server.register_function(add_tor, "add_tor")
server.register_function(pause, "pause")
server.register_function(resume, "resume")
server.register_function(retrieve, "retrieve")
server.register_function(info, "info")
server.serve_forever()
