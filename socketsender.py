from threading import Thread
import socket

class Socketsender(Thread):

    def __init__(self, host, port):
        Thread.__init__(self)

        self.host = host
        self.port = port

    def send_color_change(self, red, green, blue):

        # create a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to server and send data
            sock.connect((self.host, self.port))
            data = str(red) + "," + str(green) + "," + str(blue)
            sock.sendall(bytes(data, "utf-8"))

            # Receive data from the server
            received = str(sock.recv(1024), "utf-8")

        finally:
            sock.close()  # and shut down the server

    def run(self):
        raise NotImplementedError("Socketsenders are threads, and must have a loop to look for activity")
