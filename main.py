import machine
import utime
from tests.lcd import Lcd
from tests.encoder import Encoder


def handle_heat_action(index):
    """Akce pro menu vytápění"""
    if index == 1:
        print("PET")

    elif index == 2:
        print("PP")

def handle_cool_action(index):
    if index == 1:
        print("COOL ACTION")

class Menu:
    def __init__(self, name, menu_lines, parent=None, scrollable=True, action=None):
        self.name = name
        self.parent = parent
        self.menu = menu_lines
        self.children = {} 
        self.is_scrollable = scrollable
        self.action = action

    def add_child(self, index, child_menu):
        child_menu.parent = self
        self.children[index] = child_menu

    def execute_action(self, index):
        if self.action:
            self.action(index)

t1 = 300
t2 = 200 
t3 = 100

main = Menu("Main", [f"T1: {t1} C", f"T2: {t2} C", f"T3: {t3} C"], scrollable=False)

# Podmenu
sub = Menu("Sub", ["BACK", "HEAT UP", "COOL DOWN"])
heat = Menu("Heat", ["BACK", "PET", "PP"], action=handle_heat_action)
cool = Menu("Cool", ["BACK", "START COOLING"], action=handle_cool_action)

main.add_child(0, sub) 
main.add_child(1, sub)
main.add_child(2, sub)

sub.add_child(1, heat)
sub.add_child(2, cool) 


encoder = Encoder(clk_pin=5, dt_pin=4, sw_pin=0)
display = Lcd()

current = main
index = 0
change = True


while True:
    encoder_rotation = encoder.on_rotate()
    encoder_click = encoder.on_click()
    
    if current.is_scrollable:
        if encoder_rotation == 1:
            index = max(0, index - 1)
            change = True
        elif encoder_rotation == -1:
            index = min(len(current.menu) - 1, index + 1)
            change = True
    else:
        index = -1 

    if encoder_click == 1:
        if not current.is_scrollable:
            current = sub
            index = 0
        else:
            selected_text = current.menu[index]
            
            if selected_text == "BACK":
                if current.parent:
                    current = current.parent
                    index = 0
            elif index in current.children:
                current = current.children[index]
                index = 0
            else:
                display.clear()
                display.draw_text("PROVADIM...", 30, 25)
                display.show()
                
                current.execute_action(index)
                
                utime.sleep_ms(800) 
        
        change = True

    if change: 
        display.clear()
        
        m1 = current.menu[0] if len(current.menu) > 0 else ""
        m2 = current.menu[1] if len(current.menu) > 1 else ""
        m3 = current.menu[2] if len(current.menu) > 2 else ""
        display.draw_menu(m1, m2, m3)
        
        if current.is_scrollable and index >= 0:
            display.draw_scroll(index)
            display.draw_menu_arrows()
        
        display.draw_heating()
        if not current.is_scrollable:
            display.draw_heat_warning(90, 10, t1) 
        
        display.show()
        change = False
    
    utime.sleep_ms(10)
