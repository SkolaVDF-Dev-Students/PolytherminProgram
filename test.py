from machine import Pin, SPI
from tests.st7920 import Screen
import utime

print("Start testu...")
try:
    scr = Screen(
        sck=Pin(12), 
        mosi=Pin(11), 
        miso=Pin(14), 
        slaveSelectPin=Pin(10), 
        resetDisplayPin=Pin(13)
    )

    scr.clear()
    plot = scr.create_plotter()

    # Nakresli X pres cely displej
    for i in range(64):
        plot(i*2, i)
        plot(127-i*2, i)

    scr.redraw()
    print("Data odeslana")
except Exception as e:
    print("Chyba:", e)