import socket
from datetime import datetime
import argparse
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type = int, required = True) 
    args = parser.parse_args()
    port = args.port
    sock.bind(('127.0.0.1', port))
    print(f"Listening on UDP port {port}")
    while(True):
        data, addr = sock.recvfrom(1024)
        print(f"{datetime.now()}\Received {len(data)} bytes from {addr}: {data}")

    
main()


