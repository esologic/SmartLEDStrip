from core.stripserver import SimPins, BlasterPins, Stripserver
from core.flaskserver.uiserver import Uiserver
from core.analogcontrol import Analogcontrol

if __name__ == "__main__":

    tcp_host = "localhost"
    tcp_port = 9000

    pins = BlasterPins(17, 27, 22)  # Writes to the LEDs using the pi-blaster module, given in BCM
    analog_control = Analogcontrol(tcp_host, tcp_port)
    analog_control.start()

    strip_server = Stripserver(tcp_host, tcp_port, pins)

    ui_server = Uiserver(tcp_host, tcp_port)

    strip_server.start()
    ui_server.start()
