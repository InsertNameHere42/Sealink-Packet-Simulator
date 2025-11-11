"# UDPSimulator" 

How the frontend works:
    When the program begins, a GUI will be created which will give the user an intuitive way to configure how they want to create and send their UDP packets. They will be given choices on whether they want to create packets off of a premade table, or from files that the user can provide. They can also select the ports to send the packets to and the rate at which packets will be sent.
    The packet sending is handled in it's own seperate thread as to allow the rest of the program to run at normal speed while the packet sending thread deals with delays due to the user-inputted rate.
    When the start button is pressed, the program will create the packet-sending thread and pass the modules, rate, ports, and pattern size as parameters to create packets out of.

How the backend works:
    When packets begin to get send. The backend will create a new UDPSender object which will take in the modules, rate, ports, and pattern size. If the pattern size is -1, it will access modules through files of given file names. If the pattern size isn't equal to -1. It will access modules through a premade table of module numbers and characters.

    How the packets are created:
        First, the program will create the headers which are cnstant no matter the input.
        The program will then begin creating the payload which is done through accessing a dictionary of file names to pattern characters if reading from files. Or accessing a premade array to get a module number and pattern character. The pattern size is determined by either the size of the file being read, or the user-provided size if not reading from a file. The program will create the payload out of the three values: Module Number, Pattern Size, and Pattern Character multiplied by Pattern Size, and this will be done for each module number provided.
        After creating the payload, the program can find the size of the payload and append it to the headers. Which the payload can thus be appended to as well.
        Finally, the program will do a Cyclic Redundancy Check on the packet at this point and append the output onto the packet.
        After the CRC is appended, the packet is finished and gets sent to every port given at a given rate.