"# UDPSimulator" 

Project Objectives:
    Create an application with the ability to create and send UDP packets to an IP (in this case, the local host) with user-inputted ports to send the packets to.
    The payload of the packets will be generated off of user-decided modules which contain a character.
    Additionally, the program will be able to read files and use the file's name as the module number in the payload, the size of the file as the pattern size, and the contents of the file as the pattern character.
    The application will include a GUI for user-friendliness.
    The user will be able to connect to the existing application with an external application and TCP connection. Which will be able to send packets to the UDP applications that decide the modules to select and the rate at which to send them.

Software Structure and Choices: 
    UDP Packet Builder Backend:
        This file is used to handle the creation and sending of UDP packets. It start the packet with the headers, which are constant and cannot be changed with user input. It will then create the payload with the build_payload method has parameters for module number, pattern size, and whether the payload is being built off of a file. After creating the payload, the program will get the size of the payload to insert between the headers and payload data. Finally, the program will do a cyclic redundancy check (CRC) on the packet and append the result to the end of the packet. After the packet has been built, it is send to the local host at a given port.
    TCP Packet Builder Backend:
        This file is similar to the UDP packet builder, however, TCP packets are handled slightly differently which caused some change in syntax. How this program differentiates itself is through the contents of the payload. The payload is comprised of two main parts, separated by command codes of 0x40 and 0x41. The command code of 0x40 means that following it will be an array of Booleans converted into bytes which represent which modules the program should select. The command code of 0x41 means that the following data will represent the rate at which the program should create and send UDP packets in milliseconds. After the packet is created, it will send the data to the local host’s port 6551.
    TCP Packet Receiver Backend:
        This program will establish a connection with port 6551 and listen for TCP packets and store data based on what the payloads of the packets contained. It will collect this data by parsing through the payloads and look for the command codes to find the list of modules to enable and the rate, which will then be stored for the user.
    Main GUI:
        The MainGui file is mostly comprised of code used to build the GUI which isn’t very complex, but quite long. It does, however, contain more than just the GUI-building code. This file makes the most prominent use of object oriented programming (OOP) out of the whole project as it creates instances of the TCP packet receiver in order to take in commands from the TCP packets which can influence the configuration of UDP packets. Additionally, the GUI creates an instance of the UDP packet builder backend as it will take user input in the GUI and build packets based on those inputs. The TCP packet receiver and UDP packet builder are run in their own separate threads so as to not slow down the main GUI.


Software Used:
    Python 3.11
    Visual Studio Code 1.105.1
    Git 2.51.2
    Pyinstaller 6.16.0
    
Packet Stream Explanation:
    The UDP application will generate and send UDP packets at a constant, user inputted rate to select ports.
    The TCP application will only generate and send a single packet at a time as the program will store the last sent command and does not need a constant stream of them.

External Libraries Used:
    PyQt6

User Manual:
    The executables are held in the "dist" folder. The main application is the MainGui.exe file. It will open up a GUI which allows the user to configure how the program will generate the UDP packets. The user must decide whether to load packets from a file or from the given modules 1-5 by selecting the checkboxes titled "Pattern Size:" or "Load From File:". The user must also select which ports to send the packets to and they can also configure the rate (in milliseconds) that the packets will be sent. The user can then start sending packets.
    The TCPGui folder in "dist" contains an executable which, if the MainGui application is receiving TCP packets, will form a TCP connection with the main program and open a GUI to select which modules to use and the rate remotely. After sending the TCP Packet, pressing the "Load From Packet?" button in the main GUI will load the configuration that was sent through the TCPGui application.
    This repository also includes a UDP receiver application which can be used to test the applications. If run through the executable, it will default to listening to port 6550. However, if run in the console with the comman "python SimulateUDPReceiver.py", the user can input an argument to the end of the line formatted as "--port {input}" for the user to select a specific port to listen to.
 
