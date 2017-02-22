from stripserver import SimPins, BlasterPins, Stripserver
from flaskserver.uiserver import Uiserver

# The following way
ONPI = True
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError as e:
    ONPI = False

if __name__ == "__main__":

    if ONPI:
        pins = BlasterPins(17, 27, 22)  # Writes to the LEDs using the pi-blaster module
    else:
        pins = SimPins(5, 5, 5)  # Writes to the console (Good for developing)

    tcp_host = "localhost"
    tcp_port = 9000

    strip_server = Stripserver(tcp_host, tcp_port, pins)

    ui_server = Uiserver(tcp_host, tcp_port)

    strip_server.start()
    ui_server.start()
