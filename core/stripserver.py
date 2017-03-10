import socketserver
import os
from threading import Thread


class Pins(object):

    def __init__(self, red_led_pin, green_led_pin, blue_led_pin):
        self.pins = [red_led_pin, green_led_pin, blue_led_pin]

    def smap(self, x, in_min, in_max, out_min, out_max):
        return float((x - in_min) * (out_max - out_min)) / (in_max - in_min) + out_min

    def set_pin(self, pin, value):
        raise NotImplementedError("Must be able to change the state of a pin")


class GPIOPins(Pins):

    def __init__(self, red_led_pin, green_led_pin, blue_led_pin):
        super(GPIOPins, self).__init__(red_led_pin, green_led_pin, blue_led_pin)

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(red_led_pin, GPIO.OUT)
        GPIO.setup(green_led_pin, GPIO.OUT)
        GPIO.setup(blue_led_pin, GPIO.OUT)

        # 490Hz is close to the arduino PWM frequency
        red_pwm = GPIO.PWM(red_led_pin, 490)
        green_pwm = GPIO.PWM(green_led_pin, 490)
        blue_pwm = GPIO.PWM(blue_led_pin, 490)

        red_pwm.start(0)
        green_pwm.start(0)
        blue_pwm.start(0)

        self.pins = [red_pwm, green_pwm, blue_pwm]

    def set_pins(self, red, green, blue):
        values = [round(self.smap(red, 0, 255, 0, 100), 2),
                  round(self.smap(green, 0, 255, 0, 100), 2),
                  round(self.smap(blue, 0, 255, 0, 100), 2)]

        for pin, value in zip(self.pins, values):
            self.set_pin(pin, value)

    def set_pin(self, pin, value):
        pin.ChangeDutyCycle(value)


class BlasterPins(Pins):

    def __init__(self, red_led_pin, green_led_pin, blue_led_pin):
        super(BlasterPins, self).__init__(red_led_pin, green_led_pin, blue_led_pin)

    def set_pins(self, red, green, blue):

        red = int(red)
        green = int(green)
        blue = int(blue)

        print("Red " + str(red))
        print("Green " + str(green))
        print("Blue " + str(blue))

        values = [round(self.smap(red, 0, 255, 0, 1), 2),
                  round(self.smap(green, 0, 255, 0, 1), 2),
                  round(self.smap(blue, 0, 255, 0, 1), 2)]

        for pin, value in zip(self.pins, values):
            self.set_pin(pin, value)

    def set_pin(self, pin, value):
        os.system('echo "%d=%f" > /dev/pi-blaster' % (pin, value))


class SimPins(Pins):

    def __init__(self, red_led_pin, green_led_pin, blue_led_pin):
        super(SimPins, self).__init__(red_led_pin, green_led_pin, blue_led_pin)

    def set_pins(self, red, green, blue):
        values = [red, green, blue]

        for pin, value in zip(self.pins, values):
            self.set_pin(pin, value)

    def set_pin(self, pin, value):
        print("Setting " + str(pin) + " to " + str(value))


class Handler(socketserver.BaseRequestHandler):

    def handle(self):

        request = self.request.recv(1024)  # self.request is the TCP socket connected to the client

        print("TCP Server - Client: [" + self.client_address[0] + "] Sent: [" + str(request) + "]")

        try:
            decoded_request_string = request.decode("utf-8")
            RGB_values = decoded_request_string.split(",")

            """ This casting is more of a safety precaution, but ideally the client would send the values as ints"""
            r = int(float(RGB_values[0]))
            g = int(float(RGB_values[1]))
            b = int(float(RGB_values[2]))

            self.server.pins.set_pins(r, g, b)

        except AttributeError as error:
            raise AttributeError("Make sure you set the pins field of server after you init it! " + str(error))

        self.request.sendall(bytes("LEDs Changed", 'UTF-8'))

        print("Request filled")

class Stripserver(Thread):

    def __init__(self, host, port, pins):
        Thread.__init__(self)
        self.server = socketserver.TCPServer((host, port), Handler)
        self.server.pins = pins  # no idea if this is a hack or not
        print("Strip Server Initialized, listening on: " + str(host) + ":" + str(port))

    def run(self):
        self.server.serve_forever()






