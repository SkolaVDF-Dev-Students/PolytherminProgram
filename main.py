import machine
import utime
import network
from libs.lcd import Lcd
from libs.encoder import Encoder
from libs.rele import Rele
from libs.thermistor import Thermistor
from machine import Pin, ADC

# PROMENNE
# teploty termistoru 
t1 = 0
t2 = 0
t3 = 0

# ofset teploty termistoru, mozna uprava v LCD
offset = 35

# cilova teplota
goal_temp = 0

# LOOPY A PROGRAM
# index menu
index = 0

# nacitani displaye
change = True
t_ch = 0
l_ch = 0

# nahrivani
heating = False


# PERIFERIE
led = Pin(1, Pin.OUT)

encoder = Encoder(clk_pin=4, dt_pin=5, sw_pin=6, debounce=20)

sensor1 = Thermistor(pin_id=15, r_ref=984, v_ref=3.32, offset=offset)
sensor2 = Thermistor(pin_id=16, r_ref=984, v_ref=3.32, offset=offset)
sensor3 = Thermistor(pin_id=17, r_ref=984, v_ref=3.32, offset=offset)

display = Lcd()

rele = Rele(pin_id=2)

# zajistime ze se vypne. obcas je zaple 
rele.relay_off()


class Actions:
    @staticmethod
    def arrange(title, value, jump):
        while True:
            encoder_rotation = encoder.on_rotate()
            encoder_click = encoder.on_click()

            if encoder_rotation == -1:
                value += jump

            elif encoder_rotation == 1:
                if value > 0:
                    value -= jump

            if encoder_click == 1:
                return value
                
            display.clear()
            display.draw_settings(title, value)
            display.show()

            utime.sleep_ms(10)

    @staticmethod
    def manual_heat(index):
        """Akce pro menu vytápění"""
        global goal_temp, heating
        if index == 1:
            jump = 10

        elif index == 2:
            jump = 1

        goal_temp = Actions.arrange("GOAL TEMP", goal_temp, jump)
        heating = True


    @staticmethod
    def preset_heat(index):
        """Akce pro menu vytápění"""
        global goal_temp, heating
        if index == 1:
            goal_temp = 260

        elif index == 2:
            goal_temp = 180

        heating = True

    @staticmethod
    def settings(index):
        """Akce nastavení"""
        global offset
        if index == 1:
            offset = Actions.arrange("Offset", offset, 1)
            sensor1.set_offset(offset)
            sensor2.set_offset(offset)
            sensor3.set_offset(offset)

        elif index == 2:
            display.clear()
            display.draw_about()
            display.show() 

            while True:
                if encoder.on_click() == 1:
                    break
                
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
sub = Menu("Sub", ["BACK", "TEMP", "SETTINGS"])
temp = Menu("Temp", ["BACK", "HEAT", "COOL"])
heat = Menu("Heat", ["BACK", "MANUAL", "PRESET"])
cool = Menu("Cool", ["BACK", "START COOLING"], action=Actions.cool)
settings = Menu("Settings", ["BACK", "THERMISTOR", "ABOUT"], action=Actions.settings)
manual = Menu("Manual", ["BACK", "ARANGE 10 C", "ARANGE 1 C"], action=Actions.manual_heat)
preset = Menu("Preset", ["BACK", "PET", "PLA"], action=Actions.preset_heat)

# nastaveni deti EFN
main.add_child(0, sub) 
main.add_child(1, sub)
main.add_child(2, sub)

sub.add_child(1, temp)
sub.add_child(2, settings)

temp.add_child(1, heat)
temp.add_child(2, cool)

heat.add_child(1, manual)
heat.add_child(2, preset)

current = main

# vypnuti wifi
network.WLAN(network.STA_IF).active(False)
network.WLAN(network.AP_IF).active(False)

# boot screen
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
            if t1 >= (goal_temp - 20): 
                display.draw_info_bar(t1, goal_temp, "ready") 

            else:
                display.draw_info_bar(t1, goal_temp, "heating") 

        else:
            if t1 < 70:
                display.draw_info_bar(0, t1, "standby")

            else: 
                display.draw_info_bar(0, t1, "cooling")

        if not current.is_scrollable:
            display.draw_heat_warning(90, 10, t1, goal_temp) 
        
        display.show()
        change = False
        t_ch = 0


    # nahrivani
    if heating:
        if goal_temp > t1:
            rele.relay_on()

        else:
            rele.relay_off()

        if t1 >= (goal_temp - 20):
            led.on()


    # blikani led
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