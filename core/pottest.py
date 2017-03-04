
import spidev

spi = spidev.SpiDev()
spi.open(0, 0)

def read_adc(adcnum):
    # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout

while True:
    print(str(read_adc(0)) + ", " + str(read_adc(1)) + ", " + str(read_adc(2)))