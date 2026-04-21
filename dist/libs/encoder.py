import machine
import utime
from libs.rotary_irq_esp import RotaryIRQ

# neotestovano lol - nevadi

class Encoder:
    def __init__(self, clk_pin, dt_pin, sw_pin, debounce):
        self.r = RotaryIRQ(pin_num_clk=clk_pin, 
                          pin_num_dt=dt_pin, 
                          pull_up=True) # true = kdyz nejsou zapojeny kondiky atd. 
        
        self.sw = machine.Pin(sw_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        
        self.last_val = 0
        self.last_button = 0
        
        self._last_click_time = 0
        self._debounce_ms = debounce # debounce 200ms best (50ms trochu bugovalo), upravil sem na promenou tridy nejak se tomu rika nevim jak :D

        # IRQ pro tlacitko. rotary_irq_esp nema podporu pro tlacitko
        self.sw.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=self._click_handler)

    def on_rotate(self):
        """
        Return 1 (Clockwise), -1 (Counter clockwise) or 0 a resetuje vnittni stav.
        """
        current_val = self.r.value()
        diff = current_val - self.last_val
        self.last_val = current_val
        
        if diff > 0:
            return 1
        elif diff < 0:
            return -1
        return 0
    
    def on_click(self):
        """
        Return 1 (stisk), -1 (uvolneni), 0 (idk bracho)
        """
        value = self.last_button
        self.last_button = 0
        return value

    def _click_handler(self, pin):
        current_time = utime.ticks_ms()
        if utime.ticks_diff(current_time, self._last_click_time) < self._debounce_ms:
            return
            
        # precteme stav pomoci pullup
        if pin.value() == 0:
            self.last_button = 1
        else:
            self.last_button = -1
            
        self._last_click_time = current_time