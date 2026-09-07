from libs.st7920 import Screen
import utime

class Lcd:
    FONT = {
        'A': [0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
        'B': [0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E],
        'C': [0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E],
        'D': [0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E],
        'E': [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F],
        'F': [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10],
        'G': [0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F],
        'H': [0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
        'I': [0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E],
        'J': [0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C],
        'K': [0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11],
        'L': [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F],
        'M': [0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11],
        'N': [0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11],
        'O': [0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
        'P': [0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10],
        'R': [0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11],
        'S': [0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E],
        'T': [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
        'U': [0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
        'V': [0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04],
        'W': [0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11],
        'X': [0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11],
        'Y': [0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04],
        'Z': [0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F],
        '0': [0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E],
        '1': [0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E],
        '2': [0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F],
        '3': [0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E],
        '4': [0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02],
        '5': [0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E],
        '6': [0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E],
        '7': [0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08],
        '8': [0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E],
        '9': [0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C],
        ' ': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        '!': [0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04],
        '.': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04],
        ':': [0x00, 0x00, 0x04, 0x00, 0x04, 0x00, 0x00],
        '%': [0x18, 0x19, 0x02, 0x04, 0x08, 0x13, 0x03],
        '\x01': [0x00, 0x04, 0x06, 0x1F, 0x06, 0x04, 0x00],
        '\x02': [0x04, 0x0E, 0x1F, 0x04, 0x1C, 0x00, 0x00]
    }

    def __init__(self):
        # ESP32-S3: SCK=13, MOSI=12, CS=11, RST=14
        self.lcd = Screen(sck=13, mosi=12, cs=11, rst=14)
        self.lcd.clear()
        self.plot = self.lcd.create_plotter()

    def clear(self):
        """Clear displaye"""
        self.lcd.clear()

    def show(self):
        """Zobrazeni vseho co jsme setupovali"""
        self.lcd.redraw()

    def draw_text(self, text, x, y):
        """Vykreslení textu na souradnicich x, y"""
        for char in text.upper():
            if char in self.FONT:
                for row, byte in enumerate(self.FONT[char]):
                    for col in range(5):
                        if byte & (1 << (4 - col)):
                            self.plot(x + col, y + row)
                x += 6
        return x

    def draw_line(self, x1, y1, x2, y2):
        """Vykresleni cary od x, y do x, y"""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.plot(x1, y1)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw_rect(self, x1, y1, x2, y2):
        """Vykreslení obdélníku"""
        for x in range(x1, x2 + 1):
            self.plot(x, y1)
            self.plot(x, y2)
        for y in range(y1, y2 + 1):
            self.plot(x1, y)
            self.plot(x2, y)
    
    def draw_info_bar(self, t1, goal_temp, status):
        """Vykresli heating menicko dole"""
        self.draw_line(0, 48, 127, 48)
        if status == "heating":
            self.draw_text("HEATING", 5, 53)
            self.draw_text(str(int((t1/goal_temp)*100)), 107, 53)
            self.draw_text("%", 120, 53)
        
        elif status == "ready":
           self.draw_text("READY", 5, 53)

        elif status == "cooling":
            self.draw_text("COOLING", 5, 53)

        else:
            self.draw_text("STAND BY", 5, 53)

    def draw_menu_lines(self):
        """Vykresli cary v menu"""
        self.draw_line(0, 16, 127, 16)
        self.draw_line(0, 32, 127, 32)
        self.draw_line(0, 48, 127, 48)

    def draw_menu(self, m1, m2, m3):
        """Vykreslí texty tří položek menu"""
        self.draw_text(m1, 5, 5)
        self.draw_text(m2, 5, 21)
        self.draw_text(m3, 5, 37)

    def draw_menu_arrows(self, second):
        """Vykresli menu arrows"""
        self.draw_text("\x02", 120, 5)
        self.draw_text("\x01", 120, 21)
        if second:
            self.draw_text("\x01", 120, 37)

    def draw_heat_warning(self, x, y, t1, goal_temp):
        """Vykresli heating warning podle teploty"""
        cold_icon = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 120, 0, 8, 65, 1, 2, 84, 24, 34, 129, 2, 214, 24, 34, 129, 2, 84, 24, 33, 1, 2, 0, 24, 32, 1, 2, 0, 24, 32, 1, 2, 0, 24, 32, 1, 50, 0, 35, 16, 2, 121, 0, 79, 200, 4, 252, 128, 79, 200, 4, 252, 128, 71, 136, 2, 1, 0, 16, 32, 0, 252, 0]
        heating_icon = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 120, 56, 8, 71, 193, 2, 254, 24, 35, 129, 2, 56, 24, 35, 129, 2, 56, 24, 35, 129, 50, 56, 27, 35, 129, 50, 0, 27, 33, 193, 50, 62, 27, 35, 225, 50, 62, 35, 19, 226, 121, 62, 79, 201, 196, 252, 156, 79, 200, 4, 252, 156, 71, 137, 194, 1, 28, 16, 32, 0, 252, 0]
        hot_icon = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 120, 0, 8, 64, 1, 2, 0, 27, 32, 33, 50, 6, 27, 40, 193, 50, 216, 27, 39, 1, 50, 32, 27, 32, 1, 50, 0, 27, 33, 193, 50, 62, 27, 35, 225, 50, 62, 35, 19, 226, 121, 62, 79, 201, 196, 252, 156, 79, 200, 4, 252, 156, 71, 137, 194, 1, 28, 16, 32, 0, 252, 0]

        if t1 < 70:
            icon = cold_icon

        elif t1 < (goal_temp - 20):
            icon = heating_icon
            
        else:
            icon = hot_icon

        for row in range(30):
            for col in range(20):
                pixel_index = row * 20 + col 
                byte_index = pixel_index // 8
                bit_position = 7 - (pixel_index % 8)
                
                if byte_index < len(icon):
                    if icon[byte_index] & (1 << bit_position):
                        self.plot(x + col, y + row)

    def draw_scroll(self, index):
        """Vykresli scroll bar. Nutne zavolat v kazdem loopu. Index se vola z enkoderu"""
        if index < 0 or index > 3:
            return
        
        cell_positions = [
            (0, 16), 
            (16, 32),
            (32, 48), 
            (48, 64)  
        ]
        
        y_start, y_end = cell_positions[index]
        
        for x in range(0, 128):
            self.plot(x, y_start)
            self.plot(x, y_end - 1)

        for y in range(y_start, y_end):
            self.plot(0, y)
            self.plot(127, y)

    def draw_boot_screen(self, x, y):
        """Vykresli boot screen s logami"""

        loga = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 63, 255, 255, 127, 255, 252, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 63, 255, 255, 127, 255, 252, 0, 0, 0, 0, 0, 1, 240, 0, 0, 0, 31, 255, 255, 127, 255, 248, 0, 0, 0, 0, 0, 1, 240, 0, 0, 0, 15, 255, 255, 127, 255, 240, 0, 0, 0, 0, 0, 1, 240, 0, 0, 0, 15, 255, 255, 127, 255, 240, 0, 0, 0, 0, 0, 1, 240, 0, 0, 0, 7, 255, 255, 127, 255, 224, 0, 0, 0, 0, 0, 1, 240, 0, 0, 0, 7, 255, 255, 127, 255, 224, 0, 0, 0, 0, 0, 1, 240, 0, 0, 0, 3, 255, 255, 127, 255, 192, 0, 0, 0, 0, 0, 1, 240, 0, 0, 0, 3, 255, 255, 127, 255, 192, 0, 0, 0, 0, 0, 1, 240, 0, 0, 0, 1, 255, 128, 0, 255, 128, 0, 0, 7, 192, 0, 1, 240, 1, 254, 0, 0, 255, 192, 1, 255, 0, 0, 0, 7, 192, 0, 1, 240, 3, 252, 0, 0, 255, 224, 3, 255, 0, 0, 0, 15, 224, 3, 129, 240, 7, 240, 0, 0, 127, 224, 3, 254, 0, 0, 0, 15, 224, 31, 129, 240, 15, 224, 0, 0, 127, 240, 7, 254, 0, 0, 0, 15, 224, 255, 193, 240, 31, 192, 0, 0, 63, 248, 15, 252, 0, 0, 0, 15, 224, 255, 193, 240, 63, 128, 0, 0, 63, 248, 15, 252, 0, 0, 0, 7, 192, 255, 1, 240, 127, 0, 0, 0, 31, 224, 3, 248, 0, 0, 0, 7, 192, 0, 1, 240, 254, 0, 0, 0, 15, 140, 24, 240, 0, 0, 0, 0, 0, 0, 1, 241, 252, 0, 0, 0, 14, 60, 
30, 48, 0, 0, 0, 0, 0, 0, 1, 243, 248, 0, 0, 0, 0, 252, 31, 128, 0, 0, 0, 0, 0, 0, 1, 247, 240, 0, 0, 0, 3, 254, 63, 224, 0, 0, 0, 0, 0, 0, 1, 255, 248, 0, 0, 0, 3, 255, 127, 224, 0, 0, 0, 0, 0, 0, 1, 255, 252, 0, 0, 0, 3, 255, 127, 224, 0, 0, 0, 0, 0, 0, 1, 255, 252, 0, 0, 0, 1, 255, 255, 192, 0, 0, 0, 126, 0, 15, 193, 255, 254, 0, 0, 0, 0, 255, 255, 128, 0, 0, 0, 126, 0, 15, 193, 254, 127, 0, 0, 0, 0, 255, 255, 128, 0, 0, 0, 126, 0, 15, 193, 252, 63, 128, 0, 0, 0, 127, 255, 0, 0, 0, 0, 126, 0, 15, 193, 248, 63, 128, 0, 0, 0, 127, 255, 0, 0, 0, 0, 126, 0, 15, 129, 240, 31, 192, 0, 0, 0, 63, 254, 0, 0, 0, 0, 63, 0, 31, 129, 240, 15, 224, 0, 0, 0, 63, 254, 0, 0, 0, 0, 63, 0, 31, 129, 240, 7, 224, 0, 0, 0, 31, 252, 0, 0, 0, 0, 31, 128, 63, 1, 240, 7, 240, 
0, 0, 0, 15, 248, 0, 0, 0, 0, 31, 224, 255, 1, 240, 3, 248, 0, 0, 0, 15, 248, 0, 0, 0, 0, 15, 255, 254, 1, 240, 1, 248, 0, 0, 0, 7, 240, 0, 0, 0, 0, 7, 255, 252, 1, 240, 1, 252, 0, 0, 0, 7, 240, 0, 0, 0, 0, 3, 255, 248, 1, 240, 0, 254, 0, 0, 0, 3, 224, 0, 0, 0, 0, 0, 255, 224, 1, 240, 0, 127, 0, 0, 0, 3, 224, 0, 0, 0, 0, 0, 31, 0, 0, 0, 0, 0, 0, 0, 0, 1, 192, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for row in range(64):
            for col in range(128):
                pixel_index = row * 128 + col 
                byte_index = pixel_index // 8
                bit_position = 7 - (pixel_index % 8)
                
                if byte_index < len(loga):
                    if loga[byte_index] & (1 << bit_position):
                        self.plot(x + col, y + row)

    def draw_about(self):
        try:
            with open("/version.txt", "r") as f:
                version = f.read().strip()
                
        except:
            version = "unofficial" 

        self.draw_text("Polythermin", 5, 5)
        self.draw_text(f"Version {version}", 5, 21)
        self.draw_text("Made by SkolaVDF", 5, 37)
        self.draw_text("Licensed under MIT", 5, 53)

    def draw_settings(self, settings, var):
        self.draw_text(f"{settings}: {var}", 5, 25)