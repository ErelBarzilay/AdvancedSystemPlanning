import argparse
import sys
import struct
import socket

def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()

def run_server(ip, port):
    print("Going in")
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW)
    sock.bind(ip, port)
    conn, addr = sock.accept()
    print("connected")
    while True:
        
        data = conn.recv(1024)
        size ,data = struct.unpack("<Is",data)
        print(data)
    sock.close()



def main():
    args = get_args()
    print(args)
    run_server(args.server_ip, args.server_port)

if __name__ == '__main__':
    sys.exit(main())