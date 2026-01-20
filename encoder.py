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
        
        # Callback funkce pro události
        self._rotate_callback = None
        self._click_callback = None
        
        # Debounce tracking
        self._last_click_time = 0
        self._debounce_ms = 200

        self.clk.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self._encoder_handler)
        self.sw.irq(trigger=machine.Pin.IRQ_FALLING, handler=self._click_handler)

    def on_rotate(self, callback):
        """
        Registruje callback funkci pro otáčení enkodérem.
        
        Args:
            callback: Funkce, která bude volána s parametrem direction (1 = clockwise, -1 = anticlockwise)
        """
        self._rotate_callback = callback
    
    def on_click(self, callback):
        """
        Registruje callback funkci pro stisk tlačítka.
        
        Args:
            callback: Funkce, která bude volána bez parametrů
        """
        self._click_callback = callback

    def _encoder_handler(self, pin):
        """
        Interní handler pro detekci směru otáčení.
        Volá se automaticky při změně na CLK pinu.
        """
        current_clk = self.clk.value()
        
        if current_clk != self.last_clk_status and current_clk == 1:
            direction = -1 if self.dt.value() != current_clk else 1
            
            if self._rotate_callback:
                self._rotate_callback(direction)
                
        self.last_clk_status = current_clk

    def _click_handler(self, pin):
        """
        Interní handler pro stisk tlačítka.
        Obsahuje debounce (odrušení zákmitů).
        """
        current_time = utime.ticks_ms()
        
        # Debounce check
        if utime.ticks_diff(current_time, self._last_click_time) < self._debounce_ms:
            return
            
        utime.sleep_ms(50)
        if self.sw.value() == 0:
            self._last_click_time = current_time
            if self._click_callback:
                self._click_callback()

if __name__ == "__main__":
    # Testovací kód
    def on_rotation(direction):
        if direction == 1:
            print("CLOCKWISE")
        else:
            print("ANTICLOCKWISE")
    
    def on_button_click():
        print("MIDDLE CLICK")
    
    encoder = Encoder(clk_pin=13, dt_pin=12, sw_pin=14)
    encoder.on_rotate(on_rotation)
    encoder.on_click(on_button_click)

    while True:
        utime.sleep(1)