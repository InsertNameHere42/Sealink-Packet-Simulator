import socket
import time
import argparse
import struct
import zlib
import os

def write_payload(modules, rate):
    payload_mod = b'\x40' + bytes([int(b) for b in modules])
    payload_rate = b'\x41' + struct.pack('!H', rate)
    payload = payload_mod + payload_rate #not sure if this is how its supposed to be formatted but I can change later
    return payload
def read_payload(modules, rate): #what does read do other than different header??
    payload_mod = b'\x40' + bytes([int(b) for b in modules])
    payload_rate = b'\x41' + struct.pack('!H', rate)
    payload = payload_mod + payload_rate 
    return payload
    
class TCPSender:
    def __init__(self, host="127.0.0.1", port = 6551):
        self.on_disconnect = None
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        
    def send(self, modules, rate, reading=False):
        try:
            if reading:
                payload = read_payload(modules, rate)
                headers = b'\xAA\xDD\x00\x02'
            else:
                payload = write_payload(modules, rate)
                headers = b'\xAA\xDD\x00\x01'
                
            payload_size = len(payload)
            packet_no_crc = headers + struct.pack('!H', payload_size) + payload
            crc = zlib.crc32(packet_no_crc) & 0xffffffff
            packet = packet_no_crc + struct.pack('!I', crc) 
            
            
            self.sock.sendall(packet)
            print(f"sent packet len={len(packet)})")
        except (ConnectionResetError, BrokenPipeError, OSError) as e:
            print(f"Connection Lost: {e}")
            if self.on_disconnect:
                self.on_disconnect()


    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
            print("TCP connection closed")