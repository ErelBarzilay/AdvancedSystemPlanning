<<<<<<< HEAD
import argparse
import sys
import struct
import socket
import connection
import logging
from PIL import Image
import card
import crypt_image
###########################################################
####################### YOUR CODE #########################
###########################################################

def send_data(server_ip, server_port, data):
    sock = socket.socket()
    sock.connect((server_ip,server_port))
    data = bytearray(data, encoding = 'utf-8')
    size_data = len(data)
    to_send = struct.pack("<I"+str(size_data)+'s',size_data,data)
    sock.send(to_send)
    sock.close()
    '''
    Send data to server in address (server_ip, server_port).
    '''


###########################################################
##################### END OF YOUR CODE ####################
###########################################################

def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('name', type=str,
                        help='the name of the image')
    parser.add_argument('creator', type = str, help = 'creator of the image')
    parser.add_argument('riddle', type = str, help = 'the riddle')
    parser.add_argument('path', type = str, help = 'path to the image')

    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    img = card.Card(args.name, args.creator, crypt_image.CryptImage(Image.open(args.path)), args.riddle)
    seria = img.serialize()
    with connection.connectionContextManager(args.server_ip, args.server_port) as conn:
            conn.send_message(seria)


if __name__ == '__main__':
    sys.exit(main())
=======
import argparse
import sys
import struct
import socket
import connection
import logging
###########################################################
####################### YOUR CODE #########################
###########################################################

def send_data(server_ip, server_port, data):
    sock = socket.socket()
    sock.connect((server_ip,server_port))
    data = bytearray(data, encoding = 'utf-8')
    size_data = len(data)
    to_send = struct.pack("<I"+str(size_data)+'s',size_data,data)
    sock.send(to_send)
    sock.close()
    '''
    Send data to server in address (server_ip, server_port).
    '''


###########################################################
##################### END OF YOUR CODE ####################
###########################################################

def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('data', type=str,
                        help='the data')

    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    with connection.connectionContextManager(args.server_ip, args.server_port) as conn:
            conn.send_message(args.data)


if __name__ == '__main__':
    sys.exit(main())
>>>>>>> origin/main
