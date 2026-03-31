from machine import Pin, PWM
import time


class Piezo:
    def __init__(self, pin):
        self.__pin = PWM(Pin(pin))

    
    def click(self):
        self.__pin.freq(2000)
        self.__pin.duty_u16(30000)
        time.sleep(0.03)
        self.__pin.duty_u16(0)

    def scroll(self):
        self.__pin.freq(1700)
        self.__pin.duty_u16(20000)
        time.sleep(0.01)
        self.__pin.duty_u16(0)

    def warning(self):
        for _ in range(3):
            self.__pin.freq(1000)
            self.__pin.duty_u16(30000)
            time.sleep(0.15)
            self.__pin.duty_u16(0)
            time.sleep(0.1)

    def success(self):
        tones = [1200, 1600, 2000]

        for f in tones:
            self.__pin.freq(f)
            self.__pin.duty_u16(25000)
            time.sleep(0.08)
            self.__pin.duty_u16(0)
            time.sleep(0.02)
