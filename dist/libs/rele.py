from machine import Pin


class Rele:
    def __init__(self, pin_id):
        """
        Pin, kde je zapojeno nase rele. 
        """
        self.pin = Pin(pin_id, Pin.OUT)

    def relay_on(self):
        self.pin.value(1) 

    def relay_off(self):
        self.pin.value(0)  
