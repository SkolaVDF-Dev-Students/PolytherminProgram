# zde bude hlavni loop :()
import machine
import utime
from tests.lcd import Lcd
from tests.encoder import Encoder

# CLK -> D1 (GPIO5)
# DT  -> D2 (GPIO4)
# SW  -> D3 (GPIO0)
encoder = Encoder(clk_pin=5, dt_pin=4, sw_pin=0)

display = Lcd()

index = 0

while True:
    c = False
    rotation = encoder.on_rotate()
    click = encoder.on_click()
    
    if rotation == 1:
        index = max(0, index - 1)
        print("anticlock")
        c = True

    elif rotation == -1:
        index = min(2, index + 1)
        print("clock")
        c = True


    if click == 1:
        print("Click: Pressed")
        c = True

    if c: 
        display.clear()
        display.draw_sub_menu()
        display.draw_menu_arrows()
        display.draw_scroll(index)  
        display.draw_heating()
        display.show()