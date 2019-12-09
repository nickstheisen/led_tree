import serial
import time
import numpy as np

class LEDController:
    def __init__(self, led_count, port='/dev/ttyUSB0', baudrate=115200, timeout=1):
        self.led_count = led_count
        self.conf = np.zeros((led_count, 3), dtype=np.uint8)
        self.ser = serial.Serial(port, baudrate, timeout=timeout)

    def __del__(self):
        self.ser.close()

    def send(self):
        self.ser.write(b'\xFF'); # start byte
        self.ser.write(self.conf.reshape((3*self.led_count,)))

    def get_conf(self):
        return self.conf

    def all_on(self):
        self.conf = np.full((self.led_count, 3), 254, dtype=np.uint8)
        self.send()
        time.sleep(3);

    def all_off(self):
        self.conf = np.zeros((self.led_count, 3), dtype=np.uint8)
        self.send()
        time.sleep(3);

    def set_config(self, config):
        if self.conf.shape != config.shape:
            print("Wrong shape: {}. Correct shape: {}".format(self.conf.shape, config.shape))
            return
        if config.dtype != np.uint8:
            print("Datatype must be np.uint8.")
            return

        if config.max() >= 255:
            print("Config contains value 255. But 255 is reserved as start byte")
            return

        self.conf = config
        self.send()
