import sys
from PyQt6.QtWidgets import (QApplication, QGridLayout, QWidget, QCheckBox, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QSpinBox, QTextEdit)
from PyQt6.QtCore import Qt
from SeaLinkSimulateTCP import TCPSender

modules = [1, 2, 3, 4, 5] #might be able to just pull from the backend?



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TCP Command Generator")
        h_layout = QHBoxLayout()
        
        h_layout.addWidget(QLabel("Select Modules: "), alignment=Qt.AlignmentFlag.AlignTop)
        
        v_layout = QVBoxLayout()
        
        modules_grid = QGridLayout()
        self.mod_checkboxes = []
        for i in range(len(modules)):
            checkbox = QCheckBox(str(i+1), self)
            self.mod_checkboxes.append(checkbox)
            row = i % 2
            col = i // 2
            modules_grid.addWidget(checkbox, row, col)
                
    
    
        v_layout.addLayout(modules_grid)
        
        rate_line = QHBoxLayout()
        rate_line.addWidget(QLabel("Rate: "))
        self.rate_input = QSpinBox()
        self.rate_input.setRange(1,999)
        self.rate_input.setValue(4)
        rate_line.addWidget(self.rate_input)
        rate_line.addWidget(QLabel("ms"))
        v_layout.addLayout(rate_line)
        
        button_line = QHBoxLayout()
        self.write_button = QPushButton("Write")
        button_line.addWidget(self.write_button)
        self.read_button = QPushButton("Read")
        button_line.addWidget(self.read_button)
        v_layout.addLayout(button_line)
        
        h_layout.addLayout(v_layout)
        self.setLayout(h_layout)
        
        self.sender = TCPSender() 
        self.write_button.clicked.connect(lambda: self.sender.send(self.get_checkboxes(), self.rate_input.value(), False))
        self.read_button.clicked.connect(lambda: self.sender.send(self.get_checkboxes(), self.rate_input.value(), True))
        
        
        self.sender.on_disconnect = self.handle_disconnect
    
    def handle_disconnect(self):
        print("Closing GUI because TCP connection was aborted")
        
    def closeEvent(self, event):
        # This is called when the window is closing
        if hasattr(self, "sender") and self.sender:
            self.sender.close()
            print("TCP connection closed")
        event.accept()  # accept the close event
        
    def get_checkboxes(self):
        arr = []
        for checkbox in self.mod_checkboxes:  
            arr.append(checkbox.isChecked())
        return arr
        
                
app = QApplication(sys.argv)
window = MainWindow()
window.resize(200, 150)
window.show()
sys.exit(app.exec())
        