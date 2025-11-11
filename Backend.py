#This is the code that handles creating and sending packets on the backend. The MainGui file connects to this code.

import socket
import time
import struct
import zlib
import os

pattern_chars = {} #This is an empty dictionary that is used to hold file names as the key and the data inside the file as the value
pattern_available_chars = ['A', 'B', 'C', 'D', 'E'] #This is a premade array of pattern characters for when you aren't reading from files, you can append characters to this array and the program will run fine

def build_payload(module, size, read_file): #This method is used to build the payload that contains the module number, pattern size, and pattern character x size
    if read_file:
        pattern_char = pattern_chars[str(module)] #If reading from a file, it will access the pattern_chars dictionary for the character
    else:
        pattern_char = pattern_available_chars[module-1] #If not reading from a file, it will access the premade array
    payload = struct.pack('BB', module, size) + (pattern_char.encode() * size) #Finalizes payload before returning it
    return payload

class UDPSender:
    def __init__(self, modules, rate, ports, pattern_size):
        #Everything in the main class above is to read a single line of user input and store the data given
        if pattern_size==-1: #if the pattern_size that's given is -1, it is reading from files
            self.modules = [int(m.strip()) for m in modules] #Essentially just a loop going through an array created after splitting the String by commas and removing leading and training spaces
            for module in self.modules:
                try: #Try-Catch for file reading to store data in the pattern_chars dictionary
                    with open(str(module) + ".txt", "r") as file:
                        pattern_chars[str(module)] = file.read()
                except FileNotFoundError:
                    print(f"Error: The File '{module}.txt' was not found.")
                except Exception as e:
                    print(f"An unexpexted error occured: {e}")
                
        else:
            self.modules = modules #If not reading from files, the array of modules is already passed.
            
        self.rate = rate
        self.ports = ports
        self.pattern_size = pattern_size
    
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #constructor for socket, INET for ipv4, DGRAM for UDP
        self.running = False
        
    def get_num_available_chars(): #Just a helper method to help in creating the GUI
        return len(pattern_available_chars)


    def start(self): #Start creating and sending packets
        self.running = True
        while(self.running):
            headers = b'\xAA\xEE\x00\x00' #start with the headers
            payload = b''
            for module in self.modules: #for loop for every module in the array that was typed in
                if(self.pattern_size==-1):
                    module_size = os.path.getsize(str(module) + ".txt")
                    read_file = True
                else:
                    module_size = self.pattern_size
                    read_file = False
                payload = payload + build_payload(module, module_size, read_file) 
            payload_size = len(payload)
            packet_no_crc = headers + struct.pack('!H', payload_size) + payload #! means the most significant byte comes first and H means to two byte short
            crc = zlib.crc32(packet_no_crc) & 0xffffffff
            packet = packet_no_crc + struct.pack('!I', crc) #I means 4-byte value, like CCCC
            
            for port in self.ports: #Send a packet to every port given
                self.sock.sendto(packet, ('127.0.0.1', port))
                print(f"sent packet for modules {self.modules} len={len(packet)})")
                time.sleep(self.rate/1000) #for the rate of which its printed
            
    def stop(self):
        self.running = False
        self.sock.close()

