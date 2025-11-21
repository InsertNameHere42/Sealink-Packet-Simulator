"# UDPSimulator" 

Project Objectives:
    Create an application with the ability to create and send UDP packets to an IP (in this case, the local host) with user-inputted ports to send the packets to.
    The payload of the packets will be generated off of user-decided modules which contain a character.
    Additionally, the program will be able to read files and use the file's name as the module number in the payload, the size of the file as the pattern size, and the contents of the file as the pattern character.
    The application will include a GUI for user-friendliness.
    The user will be able to connect to the existing application with an external application and TCP connection. Which will be able to send packets to the UDP applications that decide the modules to select and the rate at which to send them.

Software Structure:
    The software is structured through multiple files and makes use of inheritance in order to create a cleaner codebase that is easier to manage and read. (not really sure what to put for structure)

Software Used:
    Python 3.11
    Visual Studio Code 1.105.1
    Git 2.51.2
    
Packet Stream Explanation:
    The UDP application will generate and send UDP packets at a constant, user inputted, rate to select ports.
    The TCP application will only generate and send a single packet at a time as the program will store the last sent command and does not need a constant stream of them.

External Libraries Used:
    PyQt6

User Manual:
    The executables are held in the "dist" folder. The main application is the MainGui.exe file. It will open up a GUI which allows the user to configure how the program will generate the UDP packets. The user must decide whether to load packets from a file or from the given modules 1-5 by selecting the checkboxes titled "Pattern Size:" or "Load From File:". The user must also select which ports to send the packets to and they can also configure the rate (in milliseconds) that the packets will be sent. The user can then start sending packets.
    The TCPGui folder in "dist" contains an executable which, if the MainGui application is receiving TCP packets, will form a TCP connection with the main program and open a GUI to select which modules to use and the rate remotely. After sending the TCP Packet, pressing the "Load From Packet?" button in the main GUI will load the configuration that was sent through the TCPGui application.
    This repository also includes a UDP receiver application which can be used to test the applications. If run through the executable, it will default to listening to port 6550. However, if run in the console with the comman "python SimulateUDPReceiver.py", the user can input an argument to the end of the line formatted as "--port {input}" for the user to select a specific port to listen to.
 
