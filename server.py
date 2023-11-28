from threading import Thread
import argparse
import sys
import struct
import socket
import card
import listener
import connection
def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()

def run_server(ip, port):
    print("Going in")
    with listener.ListenerContextManager(port,ip) as listen:
        listen.start()
        with listen.accept() as con:
            msg = con.receive_message()
            print(msg)
            print(card.Card.desirialize(msg))
    
def main():
    args = get_args()
    print(args)
    run_server(args.server_ip, args.server_port)

if __name__ == '__main__':
    sys.exit(main())