import socket
import time
import argparse
import struct
import zlib
import os

pattern_chars = {}

def build_payload(module, size):
    pattern_char = pattern_chars[str(module)]
    payload = struct.pack('BB', module, size) + (pattern_char.encode() * size)
    return payload

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--modules', required = True, help='Comma-seperated list of modules')
    parser.add_argument('--rate', type = int, required = True)
    parser.add_argument('--port', type = int, required = True)
    args = parser.parse_args()
    #Everything in the main class above is to read a single line of user input and store the data given
    modules = [int(m.strip()) for m in args.modules.split(',')] #Essentially a for loop going through an array created after splitting the String by commas and removing leading and training spaces
    for module in modules:
        try:
            with open(str(module) + ".txt", "r") as file:
                pattern_chars[str(module)] = file.read()
        except FileNotFoundError:
            print(f"Error: The File '{module}.txt' was not found.")
        except Exception as e:
            print(f"An unexpexted error occured: {e}")
    rate = args.rate
    port = args.port
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #constructor for socket, INET for ipv4, DGRAM for UDP
    
    try:
        while(True):
            packet = b'\0xAA\0xEE\0x00\0x00' #start with the headers
            payload = b''
            for module in modules: #for loop for every module in the array that was typed in
                module_size = os.path.getsize(str(module) + ".txt")
                payload = payload + build_payload(module, module_size) 
            payload_size = len(payload)
            packet_no_crc = struct.pack('!H', payload_size) + payload #! means the most significant byte comes first and H means to two byte short
            crc = zlib.crc32(packet_no_crc) & 0xffffffff
            packet = packet_no_crc + struct.pack('!I', crc) #I means 4-byte value, like CCCC
                
            sock.sendto(packet, ('127.0.0.1', port))
            print(f"sent packet for modules {modules} len={len(packet)})")
            time.sleep(rate/1000) #for the rate of which its printed
            
    except KeyboardInterrupt:
        print("Program Interrupted")


main()
    
