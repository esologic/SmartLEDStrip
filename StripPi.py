from core.stripserver import SimPins, BlasterPins, Stripserver
from core.flaskserver.uiserver import Uiserver

ONPI = True
try:
    import RPi.GPIO as GPIO
    from core.analogcontrol import Analogcontrol
except ModuleNotFoundError as e:
    ONPI = False

if __name__ == "__main__":

    tcp_host = "localhost"
    tcp_port = 9000

    if ONPI:
        pins = BlasterPins(17, 27, 22)  # Writes to the LEDs using the pi-blaster module
        analog_control = Analogcontrol(tcp_host, tcp_port)
    else:
        pins = SimPins(5, 5, 5)  # Writes to the console (Good for developing)

    strip_server = Stripserver(tcp_host, tcp_port, pins)

    ui_server = Uiserver(tcp_host, tcp_port)

    strip_server.start()
    ui_server.start()
