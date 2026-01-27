# otestovano s debounce 50ms
# nevim jak funguje :DD
# pro esp8266 zapojeni - clk pin -> D1 (GPIO5), dt pin -> D6 (GPIO12), sw pin -> D2 (GPIO4)

import machine
import utime

class Encoder:
    def __init__(self, clk_pin, dt_pin, sw_pin):
        """
        Inicializace enkodéru, nastavení pinů a přerušení.

        Args:
            clk_pin (int): GPIO pin připojený na CLK.
            dt_pin (int): GPIO pin připojený na DT.
            sw_pin (int): GPIO pin připojený na SW (tlačítko).
        """
        self.clk = machine.Pin(clk_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.dt = machine.Pin(dt_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.sw = machine.Pin(sw_pin, machine.Pin.IN, machine.Pin.PULL_UP)

        self.last_clk_status = self.clk.value()
        
        # Hodnoty pro čtení
        self.last_rotation = 0  # 1 = anticlockwise, -1 = clockwise, 0 = žádná rotace
        self.last_button = 0    # 1 = stisknuto, -1 = uvolněno, 0 = žádná změna
        
        # Debounce tracking
        self._last_click_time = 0
        self._debounce_ms = 50 # 200 ms

        self.clk.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self._encoder_handler)
        self.sw.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self._click_handler)

    def on_rotate(self):
        """
        Vrátí hodnotu rotace a resetuje ji.
        
        Returns:
            int: 1 = clockwise, -1 = anticlockwise, 0 = žádná rotace
        """
        value = self.last_rotation
        self.last_rotation = 0
        return value
    
    def on_click(self):
        """
        Vrátí hodnotu tlačítka a resetuje ji.
        
        Returns:
            int: 1 = stisknuto, -1 = uvolněno, 0 = žádná změna
        """
        value = self.last_button
        self.last_button = 0
        return value

    def _encoder_handler(self, pin):
        """
        Interní handler pro detekci směru otáčení.
        Volá se automaticky při změně na CLK pinu.
        """
        current_clk = self.clk.value()
        
        if current_clk != self.last_clk_status and current_clk == 1:
            direction = -1 if self.dt.value() != current_clk else 1
            self.last_rotation = direction  # Uložit hodnotu
                
        self.last_clk_status = current_clk

    def _click_handler(self, pin):
        """
        Interní handler pro stisk/uvolění tlačítka.
        Obsahuje debounce (odrušení zákmitů).
        """
        current_time = utime.ticks_ms()
        
        # Debounce check
        if utime.ticks_diff(current_time, self._last_click_time) < self._debounce_ms:
            return
            
        utime.sleep_ms(50)
        button_state = self.sw.value()
        
        if button_state == 0:
            self.last_button = 1  # Stisknuto
        else:
            self.last_button = -1  # Uvolněno
            
        self._last_click_time = current_time


# Testovací kód

"""
encoder = Encoder(clk_pin=5, dt_pin=12, sw_pin=4)

while True:
    rotation = encoder.on_rotate()
    click = encoder.on_click()
    
    if rotation == 1:
        print("Rotation: Anticlockwise")
    elif rotation == -1:
        print("Rotation: Clockwise")

    if click == 1:
        print("Click: Pressed")

    utime.sleep_ms(1)
"""