import socket


import argparse
import sys
from threading import Thread
import struct
import socket
import connection
def handle_con(conn, addr):
    print(connection.Connection(conn).receive_message())

class Listener:
    def __init__(self ,ip ,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
    
    def __repr__(self):
        return self.sock.repr
    
    def start(self):
        self.sock.listen(5)
    
    def stop(self):
        self.sock.close()
    
    def accept(self):
        while True:
            conn, addr = self.sock.accept()
            handle_con(conn,addr)

    @classmethod
    def start_listen(cls, port, ip):
        return Listener(ip,port)

class ListenerContextManager:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.listener = None

    def __enter__(self):
        self.listener = Listener.start_listen(self.host, self.port)
        return self.listener
    
    def __exit__(self, exc_type, exc_value, traceback):
=======
import socket


import argparse
import sys
from threading import Thread
import struct
import socket
import connection
def handle_con(conn, addr):
    print(connection.Connection(conn).receive_message())

class Listener:
    def __init__(self ,ip ,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
    
    def __repr__(self):
        return self.sock.repr
    
    def start(self):
        self.sock.listen(5)
    
    def stop(self):
        self.sock.close()
    
    def accept(self):
        while True:
            conn, addr = self.sock.accept()
            handle_con(conn,addr)

    @classmethod
    def start_listen(cls, port, ip):
        return Listener(ip,port)

class ListenerContextManager:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.listener = None

    def __enter__(self):
        self.listener = Listener.start_listen(self.host, self.port)
        return self.listener
    
    def __exit__(self, exc_type, exc_value, traceback):
>>>>>>> origin/main
        self.listener.stop()
