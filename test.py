from st7920 import Screen

# Jednoduchý 5x7 font pro písmena A-Z
FONT = {
    'A': [0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    'H': [0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    'O': [0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    'J': [0x1F, 0x04, 0x04, 0x04, 0x04, 0x14, 0x08],
    '!': [0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04],
}

def draw_char(lcd, plot, char, x, y):
    if char not in FONT:
        return x + 6
    
    for row, byte in enumerate(FONT[char]):
        for col in range(5):
            if byte & (1 << (4 - col)):
                plot(x + col, y + row)
    
    return x + 6  # Posun na další znak

def draw_text(lcd, plot, text, x, y):
    for char in text:
        x = draw_char(lcd, plot, char, x, y)

# Test
lcd = Screen()
lcd.clear()
plot = lcd.create_plotter()

draw_text(lcd, plot, "AHOJ!", 10, 10)

lcd.redraw()
