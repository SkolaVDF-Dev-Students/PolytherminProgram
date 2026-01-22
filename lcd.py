from lib import st7920
from machine import Pin

# implicitly uses hardware spi; https://docs.micropython.org/en/latest/esp8266/esp8266/quickref.html#hardware-spi-bus
screen = st7920.Screen(slaveSelectPin=Pin(15), resetDisplayPin=Pin(5))

def clear():
    screen.clear()
    screen.redraw()

def draw():

    # write zeroes to the buffer
    screen.clear()

    # draw some points, lines, rectangles, filled rectangles in the buffer
    screen.plot(5, 5)
    screen.plot(10, 10, False)
    screen.line(10, 10, 20, 20, False)
    screen.rect(25, 25, 50, 50, False)
    screen.fill_rect(5, 5, 95, 95, False)

    # send the buffer to the display
    screen.redraw()

def run():
    clear()
    draw()

run()