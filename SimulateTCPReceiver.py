import socket
from datetime import datetime
import struct
import zlib

def parse_packets(packet):
    if(len(packet)<10):
        return None, None
    
    #extract data from the packet and unpacking it
    header = packet[:4]
    payload_len = struct.unpack('!H', packet[4:6])[0]
    payload = packet[6:6+payload_len]
    crc_received = struct.unpack('!I', packet[6+payload_len:6+payload_len+4])[0]

    # Verify CRC
    crc_calc = zlib.crc32(packet[:6+payload_len]) & 0xffffffff
    if crc_calc != crc_received:
        print("CRC mismatch!")
        return None, None

    if len(payload) < 2:
        print("Payload too short")
        return None, None
    
    modules, rate = parse_payload(payload)
    
    return modules, rate

def parse_payload(payload):
    modules = []
    rate = None
    i = 0
    while i < len(payload):
        cmd = payload[i]
        i += 1
        if cmd == 0x40:
            while i < len(payload) and payload[i] not in (0x40, 0x41):
                modules.append(payload[i] != 0)
                i += 1
        elif cmd == 0x41:
            if i + 1 < len(payload):
                rate = struct.unpack('!H', payload[i:i+2])[0]
                i += 2
            else:
                print("Payload too short for rate")
                rate = None
                break
        else:
            print(f"Unknown command code: {cmd}")
            break
    return modules, rate
        


class TCPReceiver:
    def __init__(self, host="127.0.0.1", port=6551):
        self.modules = None
        self.rate = None
        self.host = host
        self.port = port
        self.connection = None
        
    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        print(f"Listening on TCP port {self.port}")
        
        self.connection, addr = self.sock.accept()
        print(f"Client connected from {addr}")
        
        while(True):
            data = self.connection.recv(1024)
            if not data:
                continue
            print(f"{datetime.now()}\Received {len(data)} bytes from {addr}: {data}")
            self.modules, self.rate = parse_packets(data)
        

        
    def stop(self):
        if self.connection:
            self.connection.close()
        self.sock.close()

    def get_modules(self):
        return self.modules
    def get_rate(self):
        return self.rate    
        


