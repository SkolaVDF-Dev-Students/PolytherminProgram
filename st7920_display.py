import machine
import utime
import framebuf

class ST7920:
    """
    Driver pro ST7920 128x64 grafický LCD displej v sériovém (SPI) režimu.
    """
    
    def __init__(self, cs_pin, sid_pin, clk_pin, rst_pin=None):
        """
        Inicializace ST7920 displeje.
        
        Args:
            cs_pin (int): GPIO pin pro CS (Chip Select)
            sid_pin (int): GPIO pin pro SID (Serial Data)
            clk_pin (int): GPIO pin pro CLK (Serial Clock)
            rst_pin (int, optional): GPIO pin pro RST (Reset)
        """
        self.cs = machine.Pin(cs_pin, machine.Pin.OUT)
        self.sid = machine.Pin(sid_pin, machine.Pin.OUT)
        self.clk = machine.Pin(clk_pin, machine.Pin.OUT)
        self.rst = machine.Pin(rst_pin, machine.Pin.OUT) if rst_pin else None
        
        self.width = 128
        self.height = 64
        
        # Framebuffer pro grafiku (128x64 pixels, 1 bit per pixel)
        self.buffer = bytearray(self.width * self.height // 8)
        self.fb = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_HLSB)
        
        self._init_display()
    
    def _write_byte(self, byte, is_data=False):
        """
        Zapíše byte přes sériové rozhraní.
        
        Args:
            byte: Byte k odeslání
            is_data: True pro data, False pro příkaz
        """
        # Synchronizace
        self._send_bits(0b11111000, 5)
        
        # RW=0 (write), RS=is_data
        if is_data:
            self._send_bits(0b11111010, 5)
        else:
            self._send_bits(0b11111000, 5)
        
        # Horní 4 bity
        self._send_bits(byte & 0xF0, 8)
        
        # Dolní 4 bity
        self._send_bits((byte << 4) & 0xF0, 8)
        
        # Čekací doba pro zpracování
        utime.sleep_us(72)  # Minimálně 72us mezi příkazy
    
    def _send_bits(self, data, count):
        """
        Odešle několik bitů přes SPI.
        """
        for i in range(count):
            self.clk.value(0)
            utime.sleep_us(2)  # ST7920 potřebuje minimálně 600ns
            self.sid.value((data >> (7 - i)) & 1)
            utime.sleep_us(2)
            self.clk.value(1)
            utime.sleep_us(2)
    
    def _init_display(self):
        """
        Inicializuje displej s potřebnými příkazy.
        """
        # Reset displeje, pokud je RST pin dostupný
        if self.rst:
            self.rst.value(0)
            utime.sleep_ms(10)
            self.rst.value(1)
            utime.sleep_ms(50)
        
        self.cs.value(1)
        utime.sleep_ms(100)
        
        # Základní konfigurace
        self._write_byte(0x30)  # 8-bit interface, základní instrukce
        utime.sleep_ms(2)
        self._write_byte(0x30)  # Opakovat
        utime.sleep_ms(2)
        self._write_byte(0x0C)  # Displej ON, kurzor OFF
        utime.sleep_ms(2)
        self._write_byte(0x01)  # Vyčistit displej
        utime.sleep_ms(10)
        self._write_byte(0x06)  # Entry mode: increment, no shift
        utime.sleep_ms(2)
        
        # Přepnout do grafického režimu
        self._write_byte(0x36)  # Extended instructions, graphics ON
        utime.sleep_ms(2)
        self._write_byte(0x36)  # Opakovat pro jistotu
        utime.sleep_ms(2)
        
        self.clear()
    
    def clear(self):
        """
        Vyčistí framebuffer (ne displej).
        """
        self.fb.fill(0)
    
    def update(self):
        """
        Pošle framebuffer na displej.
        """
        # ST7920 má GDRAM rozdělenou na dvě poloviny (horní a dolní)
        for y in range(32):
            # Horní polovina (Y = 0-31)
            self._set_gdram_address(y, 0)
            for x in range(16):
                idx = y * 16 + x
                self._write_byte(self.buffer[idx], is_data=True)
        
        for y in range(32):
            # Dolní polovina (Y = 32-63)
            self._set_gdram_address(y, 1)
            for x in range(16):
                idx = (y + 32) * 16 + x
                self._write_byte(self.buffer[idx], is_data=True)
    
    def _set_gdram_address(self, y, half):
        """
        Nastaví GDRAM adresu pro zápis.
        
        Args:
            y: Y souřadnice (0-31)
            half: 0 pro horní polovinu, 1 pro dolní polovinu
        """
        # Příkaz pro nastavení vertikální adresy
        self._write_byte(0x80 | y)
        # Příkaz pro nastavení horizontální adresy
        self._write_byte(0x80 | half)
    
    def pixel(self, x, y, color):
        """
        Nastaví pixel na souřadnicích x, y.
        
        Args:
            x: X souřadnice (0-127)
            y: Y souřadnice (0-63)
            color: 1 = ON, 0 = OFF
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.fb.pixel(x, y, color)
    
    def text(self, text, x, y, color=1):
        """
        Vykreslí text na pozici x, y.
        
        Args:
            text: Text k vykreslení
            x: X souřadnice
            y: Y souřadnice
            color: 1 = bílá, 0 = černá
        """
        self.fb.text(text, x, y, color)
    
    def line(self, x0, y0, x1, y1, color=1):
        """
        Nakreslí čáru mezi dvěma body.
        """
        self.fb.line(x0, y0, x1, y1, color)
    
    def rect(self, x, y, w, h, color=1, fill=False):
        """
        Nakreslí obdélník.
        """
        if fill:
            self.fb.fill_rect(x, y, w, h, color)
        else:
            self.fb.rect(x, y, w, h, color)
    
    def hline(self, x, y, length, color=1):
        """
        Nakreslí vodorovnou čáru.
        """
        self.fb.hline(x, y, length, color)
    
    def vline(self, x, y, length, color=1):
        """
        Nakreslí svislou čáru.
        """
        self.fb.vline(x, y, length, color)
    
    def invert_rect(self, x, y, w, h):
        """
        Invertuje pixely v obdélníkové oblasti (pro zvýraznění).
        """
        for py in range(y, min(y + h, self.height)):
            for px in range(x, min(x + w, self.width)):
                current = self.fb.pixel(px, py)
                self.fb.pixel(px, py, 1 - current)


if __name__ == "__main__":
    # Testovací kód
    display = ST7920(cs_pin=5, sid_pin=4, clk_pin=0, rst_pin=2)
    
    # Test vykreslování
    display.clear()
    display.text("ST7920 Test", 10, 0)
    display.text("128x64 LCD", 10, 10)
    display.rect(0, 0, 128, 64, 1)
    display.line(0, 0, 127, 63, 1)
    display.update()
    
    print("Display initialized and test pattern drawn")
