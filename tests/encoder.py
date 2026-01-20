import machine
import utime

# Setup Pins
clk = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP) # D5 / GPIO13
dt = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP) # D6 / GPIO12
sw = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP) # D7 / GPIO14

last_clk_status = clk.value()

def encoder_handler(pin):
    global last_clk_status
    current_clk = clk.value()
    
    # Only trigger when the signal changes
    if current_clk != last_clk_status and current_clk == 1:
        if dt.value() != current_clk:
            print("CLOCKWISE")
        else:
            print("ANTICLOCKWISE")
            
    last_clk_status = current_clk

def click_handler(pin):
    # Debounce: wait 50ms and check if still pressed
    utime.sleep_ms(50)
    if pin.value() == 0:
        print("MIDDLE CLICK")

# Set up Interrupts
# Should we use polling instead later?
clk.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=encoder_handler)
sw.irq(trigger=machine.Pin.IRQ_FALLING, handler=click_handler)

while True:
    # Keep the script alive
    utime.sleep(1)