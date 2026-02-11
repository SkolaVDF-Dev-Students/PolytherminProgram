import machine
import utime
from tests.lcd import Lcd
from tests.encoder import Encoder
from tests.rele import Rele

t1 = 10
t2 = 200 
t3 = 100

goal_temp = 0

index = 0
change = True
heating = False

encoder = Encoder(clk_pin=5, dt_pin=4, sw_pin=0)
display = Lcd()
rele = Rele(2)
rele.relay_off()


def handle_preset_heat_action(index):
    global goal_temp, heating 
    """Akce pro menu vytápění"""
    if index == 1:
        goal_temp = 300
        heating = True

    elif index == 2:
        goal_temp = 250
        heating = True

def handle_manual_heat_action(index):
    """Akce pro menu vytápění"""
    global goal_temp, heating
    if index == 1:
        while True:
            encoder_rotation = encoder.on_rotate()
            encoder_click = encoder.on_click()

            if encoder_rotation == -1:
                goal_temp += 10

            elif encoder_rotation == 1:
                if goal_temp > 0:
                    goal_temp -= 10

            if encoder_click == 1:
                heating = True
                break
            
            display.clear()
            display.draw_heat_settings(goal_temp)
            display.show()   

            utime.sleep_ms(10)  

    elif index == 2:
        while True:
            encoder_rotation = encoder.on_rotate()
            encoder_click = encoder.on_click()
            if encoder_rotation == -1:
                goal_temp += 1

            elif encoder_rotation == 1:
                if goal_temp > 0:
                    goal_temp -= 1
            
            if encoder_click == 1:
                heating = True
                break

            display.clear()
            display.draw_heat_settings(goal_temp)
            display.show() 

            utime.sleep_ms(10)   

            

def handle_cool_action(index):
    """Start cooling"""
    global heating
    if index == 1:
        heating = False
        rele.relay_off()
        print("TURNING RELAY OFF")

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


main = Menu("Main", [f"T1: {t1} C", f"T2: {t2} C", f"T3: {t3} C"], scrollable=False)

# Podmenu
sub = Menu("Sub", ["BACK", "HEAT UP", "COOL DOWN"])
heat = Menu("Heat", ["BACK", "PRESET", "MANUAL"])
preset = Menu("Heat", ["BACK", "PET", "PP"], action=handle_preset_heat_action)
manual = Menu("Heat", ["BACK", "ARANGE 10 C", "ARANGE 1 C"], action=handle_manual_heat_action)
cool = Menu("Cool", ["BACK", "START COOLING", ""], action=handle_cool_action)

main.add_child(0, sub) 
main.add_child(1, sub)
main.add_child(2, sub)

sub.add_child(1, heat)
sub.add_child(2, cool)

heat.add_child(1, preset)
heat.add_child(2, manual)


current = main


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
                change = True
                current.execute_action(index)

        change = True

    if change: 
        display.clear()
        
        m1 = current.menu[0] if len(current.menu) > 0 else ""
        m2 = current.menu[1] if len(current.menu) > 1 else ""
        m3 = current.menu[2] if len(current.menu) > 2 else ""
        display.draw_menu(m1, m2, m3)
        
        if current.is_scrollable and index >= 0:
            display.draw_scroll(index)
            display.draw_menu_arrows(True)
        
        display.draw_heating()
        if not current.is_scrollable:
            display.draw_heat_warning(90, 10, t1) 
        
        display.show()
        change = False


    if heating:
        # 300 > 300
        if goal_temp >= t1:
            rele.relay_on()
            print("RELAY IS ON")

        else:
            print("TURNING RELAY OFF")
            rele.relay_off()
    
    utime.sleep_ms(10)
