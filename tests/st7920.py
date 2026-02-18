from machine import Pin, SPI
from time import sleep

# Rozměry framebufferu
rowBound = 64
colBound = 128 // 8

class Screen:
    def __init__(self, sck=12, mosi=11, cs=10, rst=13, baudrate=1000000):
        # Inicializace SPI na ESP32-S3 (Hardwarové SPI2)
        # S3 vyžaduje definici pinů přímo v konstruktoru SPI
        self.spi = SPI(2, baudrate=baudrate, polarity=0, phase=0, sck=Pin(sck), mosi=Pin(mosi))
        
        self.cs = Pin(cs, Pin.OUT)
        self.rst = Pin(rst, Pin.OUT)
        
        self.cmdbuf = bytearray(33)
        self.cmdmv = memoryview(self.cmdbuf)
        
        # Buffer pro grafiku
        self.fbuff = [memoryview(bytearray(colBound)) for _ in range(rowBound)]
        
        self.rot = 0
        self.width = 128
        self.height = 64
        
        self.config()

    def config(self):
        self.reset()
        self.select(True)
        
        # Sekvence příkazů pro ST7920
        self.send_flag(0x30)  # Basic instruction set
        sleep(0.01)
        self.send_flag(0x30)  # Repeated
        self.send_flag(0x0C)  # Display on
        
        self.send_flag(0x34)  # Extended instruction set (RE=1)
        self.send_flag(0x36)  # Graphics display ON
        
        self.select(False)

    def select(self, selected):
        self.cs.value(1 if selected else 0)

    def reset(self):
        self.rst.value(0)
        sleep(0.1)
        self.rst.value(1)
        sleep(0.1)

    def send_flag(self, b):
        self.cmdbuf[0] = 0b11111000  # RS=0, RW=0
        self.cmdbuf[1] = b & 0xF0
        self.cmdbuf[2] = (b & 0x0F) << 4
        self.spi.write(self.cmdmv[:3])

    def send_address(self, b1, b2):
        self.cmdbuf[0] = 0b11111000
        self.cmdbuf[1] = b1 & 0xF0
        self.cmdbuf[2] = (b1 & 0x0F) << 4
        self.cmdbuf[3] = b2 & 0xF0
        self.cmdbuf[4] = (b2 & 0x0F) << 4
        self.spi.write(self.cmdmv[:5])

    def send_data(self, arr):
        arrlen = len(arr)
        count = 1 + (arrlen * 2)
        self.cmdbuf[0] = 0b11111010  # RS=1, RW=0
        for i in range(arrlen):
            self.cmdbuf[1 + (i * 2)] = arr[i] & 0xF0
            self.cmdbuf[2 + (i * 2)] = (arr[i] & 0x0F) << 4
        self.spi.write(self.cmdmv[:count])

    def clear(self):
        for row in self.fbuff:
            for i in range(len(row)):
                row[i] = 0

    def create_plotter(self):
        def plot(x, y):
            if 0 <= x < 128 and 0 <= y < 64:
                self.fbuff[y][x // 8] |= 1 << (7 - (x % 8))
        return plot

    def redraw(self):
        self.select(True)
        for i in range(64):
            # ST7920 adresování: 0-31 horní polovina, 32-63 spodní polovina
            y_addr = 0x80 + (i % 32)
            x_addr = 0x80 + (0 if i < 32 else 8)
            self.send_address(y_addr, x_addr)
            self.send_data(self.fbuff[i])
        self.select(False)