#This code is what handles to frontend of the program, it creates a GUI and sends data that the user inputs to the GUI to the backend

import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QCheckBox, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QSpinBox, QTextEdit)
from PyQt6.QtCore import QThread, pyqtSignal
from Backend import UDPSender
from SimulateTCPReceiver import TCPReceiver



class SenderThread(QThread): #The code that handles sending data to the backend. It's run on it's own thread so as to not slow down the rest of the program
    log = pyqtSignal(str)
    def __init__(self, modules, rate, port, read_file):
        super().__init__()
        self.modules = modules
        self.rate = rate
        self.port = port
        self.read_file = read_file
        self.sender = UDPSender(modules, rate, port, read_file)
    
    def run(self):
        self.log.emit("Sender Started.")
        try:
            self.sender.start()
        except Exception as e:
            self.log.emit(f"Error: {e}")
        self.log.emit("Sender Stopped")
        
    def stop(self): 
        if self.sender:
            self.sender.stop()
    
class ReceiverThread(QThread):
    log = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.receiver = TCPReceiver()
        
    def run(self):
        self.log.emit("Receiver Started.")
        try:
            self.receiver.start()
        except Exception as e:
            self.log.emit(f"Error {e}")
        self.log.emit("Receiver Stopped")
        self.receiving = False
        
    
    def stop(self):
        if self.receiver:
            self.receiver.stop()
        self.quit()
        self.wait()
        

        
class MainWindow(QWidget): #This class handles creating the GUI
    def __init__(self):
        self.sending = False
        self.receiving = False
        super().__init__()
        self.setWindowTitle("Sealink Packet Simulator")
        self.thread = None
        self.rThread = None #Receiver Thread
        
        
        v_layout = QVBoxLayout()
        h_box1 = QHBoxLayout()
        module_label = QLabel("Select Modules:")
        module_label.setStyleSheet("font-size: 16px;") 
        h_box1.addWidget(module_label)
        self.mod_checkboxes = []
        for i in range (UDPSender.get_num_available_chars()):
            checkbox = QCheckBox(str(i+1), self)
            checkbox.setStyleSheet("font-size: 16px;")
            self.mod_checkboxes.append(checkbox)
            h_box1.addWidget(checkbox)

        
        h_box2 = QHBoxLayout()
        h_box2.setContentsMargins(0, 0, 0, 0)
        h_box2.setSpacing(5)
        self.no_file_checkbox = QCheckBox(self)
        h_box2.addWidget(self.no_file_checkbox)
        pattern_size_label = QLabel("Pattern Size:")
        pattern_size_label.setStyleSheet("font-size: 16px;") 
        h_box2.addWidget(pattern_size_label)
        self.pattern_size_input = QSpinBox()
        self.pattern_size_input.setRange(0, 99)
        self.pattern_size_input.setValue(20)
        self.pattern_size_input.setStyleSheet("border: 2px solid #4FE0DD; background: white;")
        h_box2.addWidget(self.pattern_size_input)
        self.file_checkbox = QCheckBox(self)
        h_box2.addWidget(self.file_checkbox)
        h_box2.addWidget(QLabel("Load From File:"))
        self.modules_input = QLineEdit()
        self.modules_input.setStyleSheet("border: 2px solid #4FE0DD; background: white;")
        h_box2.addWidget(self.modules_input)
        self.receive_TCP = QPushButton("Receive TCP?")
        self.receive_TCP.setStyleSheet("background-color: lime;")
        h_box2.addWidget(self.receive_TCP)
        self.TCP_input = QPushButton("Load from packet?")
        self.TCP_input.setStyleSheet("background-color: #4FE0DD;")
        
        h_box2.addWidget(self.TCP_input)
        
        
        h_box3 = QHBoxLayout()
        hb3_v_box1 = QVBoxLayout() #horizontal box 3 v box 1
        self.port_checkboxes = []
        self.port_options = []
        for i in range(4):
            temp_h_box = QHBoxLayout()
            temp_checkbox = QCheckBox(f"Port {i+1}", self)
            temp_checkbox.setStyleSheet("font-size: 16px;")
            self.port_checkboxes.append(temp_checkbox)
            temp_h_box.addWidget(temp_checkbox)
            port_option = QSpinBox()
            port_option.setRange(1, 65535)
            port_option.setValue(6550 + 10*i)
            port_option.setStyleSheet("border: 2px solid #4FE0DD; background: white;")
            self.port_options.append(port_option)
            temp_h_box.addWidget(port_option)
            hb3_v_box1.addLayout(temp_h_box)
        
    
        hb3_v_box2 = QVBoxLayout()
        hb3vb2_h_box1 = QHBoxLayout()
        hb3vb2_h_box1.addWidget(QLabel("Rate: "))
        self.rate_input = QSpinBox()
        self.rate_input.setRange(1,999)
        self.rate_input.setValue(10)
        self.rate_input.setStyleSheet("border: 2px solid #4FE0DD; background: white")
        hb3vb2_h_box1.addWidget(self.rate_input)
        hb3vb2_h_box1.addWidget(QLabel("ms"))
        
        
        self.start_stop_btn = QPushButton("Start")
        self.start_stop_btn.setStyleSheet("background-color: lime; font-size: 16px;")
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True) #output box
        self.log_area.setStyleSheet("background-color: black; color: white; border: 2px solid #4FE0DD;")
        hb3_v_box2.addWidget(self.log_area)
        hb3_v_box2.addWidget(self.start_stop_btn)

        h_box3.addLayout(hb3_v_box1)
        
        hb3_v_box2.addLayout(hb3vb2_h_box1)
        h_box3.addLayout(hb3_v_box2)
        
        v_layout.addLayout(h_box1)
        v_layout.addLayout(h_box2)
        v_layout.addLayout(h_box3)
        self.setLayout(v_layout)
        
        self.receive_TCP.clicked.connect(self.toggle_receiving)
        self.start_stop_btn.clicked.connect(self.toggle_sending)
        self.TCP_input.clicked.connect(self.TCP_update)


    def TCP_update(self):
        if self.receiving and self.rThread.receiver.get_modules() != None and self.rThread.receiver.get_rate() !=None:
            TCP_modules = self.rThread.receiver.get_modules()
            TCP_rate = self.rThread.receiver.get_rate()
            for i in range(len(self.mod_checkboxes)):
                self.mod_checkboxes[i].setChecked(TCP_modules[i])
            self.rate_input.setValue(TCP_rate)
        
    def toggle_receiving(self):
        if self.receiving:
            if self.rThread:
                self.rThread.stop()
            self.receiving = False
            self.receive_TCP.setText("Receive TCP?")
            self.receive_TCP.setStyleSheet("background-color: lime;")
        else:
            self.rThread = ReceiverThread()
            self.rThread.log.connect(self.log_area.append)
            self.rThread.start()
            self.receiving = True
            self.receive_TCP.setText("Stop Receiving TCP?")
            self.receive_TCP.setStyleSheet("background-color: red;")
            
        
    def toggle_sending(self): #Pressing the start/stop button calls this method to create a SenderThread to start sending data to the backend.
        if self.sending:
            if self.thread:
                self.thread.stop()
                self.thread.wait()
            self.sending = False
            self.start_stop_btn.setText("Start")
            self.start_stop_btn.setStyleSheet("background-color: lime;")
        else:
            ports = []
            if(not self.file_checkbox.isChecked() and not self.no_file_checkbox.isChecked()):
                self.log_area.append("Error: No Module Input Selected")
            else:
                if(self.no_file_checkbox.isChecked()): #This takes priority over reading from files if both are checked
                    modules = []
                    pattern_size = self.pattern_size_input.value()
                    for i in range(len(self.mod_checkboxes)): #Reads which modules were checked
                        if self.mod_checkboxes[i].isChecked():
                            modules.append(i+1) #i+1 here to make the "sent packet for modules..." output text look correct instead of saying module 0 when 1 is selected. The backend handles it correctly to not cause an index out of bounds error
                elif(self.file_checkbox.isChecked()):
                    pattern_size = -1 #Set pattern size to -1 so the backend knows to read from files
                    modules = [m.strip() for m in self.modules_input.text().split(',') if m.strip()]
                rate = self.rate_input.value()
                for i in range(len(self.port_checkboxes)): #Checks which ports to send packets to
                    if self.port_checkboxes[i].isChecked():
                        ports.append(self.port_options[i].value())
            
            
                self.thread = SenderThread(modules, rate, ports, pattern_size)
                self.thread.log.connect(self.log_area.append)
                self.thread.start()
                self.sending = True
                self.start_stop_btn.setText("Stop")
                self.start_stop_btn.setStyleSheet("background-color: red;")
        
        
            
app = QApplication(sys.argv)
window = MainWindow()
window.resize(800, 400)
window.setStyleSheet("background-color: #AEAFBD")
window.show()
sys.exit(app.exec())
        

        