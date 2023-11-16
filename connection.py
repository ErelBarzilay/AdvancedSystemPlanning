import argparse
import sys
from threading import Thread
import struct
import socket
###########################################################
####################### YOUR CODE #########################
###########################################################
def handle_con(conn):
    data = conn.recv(1024)
    size = struct.unpack_from("<I",data)
    print(size[0])
    data = struct.unpack("<I"+str(size[0])+"s",data)
    return (data[1].decode('utf-8'))
    
class Connection:
    def __init__(self, sock):
        self.con = sock

    def __repr__(self):
        return self.con.repr()
    
    def close(self):
        self.con.close()
    
    def send_message(self, data):
        data = bytearray(data, encoding = 'utf-8')
        size_data = len(data)
        to_send = struct.pack("<I"+str(size_data)+'s',size_data,data)
        self.con.send(to_send)
    '''
    Send data to server in address (server_ip, server_port).
    '''
    
    @classmethod
    def connect(cls, host, port): #note that using this function means we're in the client case!!!
        sock = socket.socket()
        sock.connect((host,port))
        return Connection(sock)
 

    def receive_message(self):
        # assume we're connected
        return handle_con(self.con)
    
class connectionContextManager:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None
    def __enter__(self):
        self.connection = Connection.connect(self.host,self.port)
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()
        
