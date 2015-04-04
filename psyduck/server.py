import pyaudio
import socket
from thread import *
import sys
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
host = ''
port = 5000
backlog = 10
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)

def clientthread(client):
    while True:
        client.send('Connected to server\n')
        print ''.join(map(str,client)) + " has entered connection !"
        data = client.recv(size)
        print data

while True:
    client, address = s.accept()
    start_new_thread(clientthread,(client,))

    #window
    class Window(QtGui.QMainWindow):
        def __init__(self):
            QtGui.QWidget.__init__(self)
            self.resize(250, 350)
            self.move(200, 300)
            self.setWindowTitle('Server')
            self.setStyleSheet("QMainWindow { background: 'black'}")
            self.button = QtGui.QPushButton('Call', self)
            self.button.resize(100,30)
            self.button.move(75,175)
            self.button.clicked.connect(self.handleButton)
            layout = QtGui.QVBoxLayout(self)
            layout.addWidget(self.button)

        def handleButton(self):
            while 1:
                data = stream.read(chunk)
                client.send(data)
                client.recv(size)

    if __name__ == '__main__':
        app = QtGui.QApplication(sys.argv)

        w = Window()
        w.show()

        sys.exit(app.exec_())


        
# Main Functionality


client.close()
stream.close()
p.terminate()

