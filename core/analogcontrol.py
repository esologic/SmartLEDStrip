import socket
import sys
from time import sleep
import spidev
from threading import Thread
from core.socketsender import Socketsender
from datetime import datetime

class Analogcontrol(Socketsender):

    def __init__(self, host, port):
        Socketsender.__init__(self, host, port)

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)

        print("Init analog Control")


    def s_map(self, x, in_min, in_max, out_min, out_max):
        return ((x - in_min) * (out_max - out_min)) / (in_max - in_min) + out_min

    def read_adc(self, adcnum):
        # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
        if adcnum > 7 or adcnum < 0:
            return -1
        r = self.spi.xfer2([1, 8 + adcnum << 4, 0])
        adcout = ((r[1] & 3) << 8) + r[2]
        return adcout

    def run(self):

        sample_count = 0
        max_samples = 500

        sample_sets = [[], [], []]
        previous_colors = [0, 0, 0]

        while True:

            count = 0

            for samples, previous_color in zip(sample_sets, previous_colors):

                sample = int(self.s_map(self.read_adc(count), 0, 1024, 0, 255))

                try:
                    samples[sample_count] = sample
                except IndexError:
                    samples.append(sample)

                sample_count += 1

                if sample_count == max_samples:
                    sample_count = 0

                value = int(sum(samples)/len(samples))

                if value != previous_color and abs(value-previous_color) > 15:
                    print(count)
                    previous_colors[count] = value
                    print("Sending color")

                    self.send_color_change(previous_colors[0], previous_colors[1], previous_colors[2])

                count += 1