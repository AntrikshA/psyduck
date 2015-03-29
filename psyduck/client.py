import pyaudio
import socket
import sys
import time
from PyQt4 import QtGui, QtCore, uic
import sys

# Pyaudio Initialization
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 10240

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                output = True,
                input = True,
                frames_per_buffer = chunk)

# Socket Initialization
host = 'localhost'
port = 50000
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
print "Client connected..."

#window
class CallWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(250, 350)
        self.move(700, 300)
        self.setWindowTitle('Client')
        self.setStyleSheet("QWidget { background: 'black'}")
        caller = "Server Calling ..."
        print caller
        self.text = QtGui.QStaticText(caller)
        self.button = QtGui.QPushButton('Disconnect', self)
        self.button.resize(75,30)
        self.button.move(105,200)
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.disconnect)

        self.button = QtGui.QPushButton('Attend', self)
        self.button.resize(75,30)
        self.button.move(20,150)
        self.button.clicked.connect(self.attendCall)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.button)

    def attendCall(self):
        while 1:            
            data = s.recv(size)
            if data:
                #Write data to pyaudio stream
                stream.write(data)  # Stream the recieved audio data
                s.send('ACK')  # Send an ACK
                
    def disconnect(self):
        print "Disconnecting..."
        self.deleteLater()

class Window(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.resize(250, 350)
        self.move(700, 300)
        self.setWindowTitle('Client')

    def handleButton(self):
        while 1:
            data = stream.read(chunk)
            s.send(data)
            s.recv(size)

# Main Functionality
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
        
    w = Window()
    w.show()
    if s.recv(size):
        call = CallWindow()
        call.show()
    sys.exit(app.exec_())

s.close()
stream.close()
p.terminate()
