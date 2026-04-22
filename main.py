import machine
import utime
import network
from libs.lcd import Lcd
from libs.encoder import Encoder
from libs.rele import Rele
from libs.thermistor import Thermistor
from machine import Pin, ADC

# PROMENE
# teploty termistoru 
t1 = 0
t2 = 0
t3 = 0

# cilova teplota
goal_temp = 0

# globalni promene na optimalizaci
index = 0

# optimalizace nacitani
change = True
heating = False
t_ch = 0
l_ch = 0


# PERIFERIE
led = Pin(1, Pin.OUT)

encoder = Encoder(clk_pin=4, dt_pin=5, sw_pin=6, debounce=20)

sensor1 = Thermistor(pin_id=15, r_ref=984.0, v_ref=3.32, offset=35)
sensor2 = Thermistor(pin_id=16, r_ref=984.0, v_ref=3.32, offset=35)
sensor3 = Thermistor(pin_id=17, r_ref=984.0, v_ref=3.32, offset=35)

display = Lcd()

rele = Rele(pin_id=2)

# zajistime ze se vypne. obcas je zaple 
rele.relay_off()


# akce v menu 
class Actions:
    @staticmethod
    def preset_heat(index):
        global goal_temp, heating 
        """Akce pro menu vytápění"""
        if index == 1:
            goal_temp = 300
            heating = True

        elif index == 2:
            goal_temp = 250
            heating = True

    @staticmethod
    def manual_heat(index):
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

                
    @staticmethod
    def cool(index):
        """Start cooling"""
        global heating
        if index == 1:
            heating = False
            rele.relay_off()


# menu nastaveni parent atd.
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

    def change_temp(self, t1, t2, t3):
        self.menu = [f"T1: {int(t1)} C", f"T2: {int(t2)} C", f"T3: {int(t3)} C"]


# nastaveni main menu
main = Menu("Main", [f"T1: {int(t1)} C", f"T2: {int(t2)} C", f"T3: {int(t3)} C"], scrollable=False)

# podmenu
sub = Menu("Sub", ["BACK", "HEAT UP", "COOL DOWN"])
heat = Menu("Heat", ["BACK", "PRESET", "MANUAL"])
preset = Menu("Heat", ["BACK", "PET", "PP"], action=Actions.preset_heat)
manual = Menu("Heat", ["BACK", "ARANGE 10 C", "ARANGE 1 C"], action=Actions.manual_heat)
cool = Menu("Cool", ["BACK", "START COOLING"], action=Actions.cool)

# nastaveni deti EFN
main.add_child(0, sub) 
main.add_child(1, sub)
main.add_child(2, sub)

sub.add_child(1, heat)
sub.add_child(2, cool)

heat.add_child(1, preset)
heat.add_child(2, manual)


current = main

# vypnuti wifi
network.WLAN(network.STA_IF).active(False)
network.WLAN(network.AP_IF).active(False)

# boot screen - tu udelat async - naser si :)
display.clear()
display.draw_boot_screen(0, 0)
display.show()
utime.sleep(3)


while True:
    # cteni periferii
    encoder_rotation = encoder.on_rotate()
    encoder_click = encoder.on_click()
    t1 = sensor1.read()
    t2 = sensor2.read()
    t3 = sensor3.read()

    
    # zda jsme v main menu
    if current.is_scrollable:
        if encoder_rotation == 1:
            index = max(0, index - 1)
            change = True
        elif encoder_rotation == -1:
            index = min(len(current.menu) - 1, index + 1)
            change = True
    else:
        index = -1 


    # vyhodnoceni enkoderu
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


    # update screenu kazde 1s nebo po interakci
    if change or (t_ch == 100): 
        display.clear()

        main.change_temp(t1, t2, t3)
        
        m1 = current.menu[0] if len(current.menu) > 0 else ""
        m2 = current.menu[1] if len(current.menu) > 1 else ""
        m3 = current.menu[2] if len(current.menu) > 2 else ""
        display.draw_menu(m1, m2, m3)
        
        if current.is_scrollable and index >= 0:
            display.draw_scroll(index)
            if m3 != "":
                display.draw_menu_arrows(True)
            else:
                display.draw_menu_arrows(False)
        
        if heating:
            if t1 >= (goal_temp - 10): 
                display.draw_info_bar(t1, goal_temp, "ready") 

            else:
                display.draw_info_bar(t1, goal_temp, "heating") 

        else:
            if t1 < 30:
                display.draw_info_bar(0, t1, "standby")

            else: 
                display.draw_info_bar(0, t1, "cooling")

        if not current.is_scrollable:
            display.draw_heat_warning(90, 10, t1) 
        
        display.show()
        change = False
        t_ch = 0


    # nahrivani toto potreba optimalizovat
    if heating:
        if goal_temp > t1:
            rele.relay_on()

        else:
            rele.relay_off()

        if t1 >= (goal_temp - 10):
            led.on()


    if t1 > 70:
        if l_ch == 100:
            led.on()

        elif l_ch == 200:
            led.off()
            l_ch = 0

    else:
        led.off()
        


    l_ch += 1
    t_ch += 1

    utime.sleep_ms(10)