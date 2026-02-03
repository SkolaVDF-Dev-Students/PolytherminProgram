# zde bude hlavni loop :()
# pridano komenty pro nejake saski co to budou cist. doufam ze chapete jinak mi poslete klicenku. pokud tento komentar nevidis nejsi v feature/ui branchy - chyba switchni do feature/ui.
# jeste jednou piste vse do tohoto branche ja az prijdu v pondeli checknu to a mergnu to do main. dekujeme budoucimu misovi.
import machine
import utime
from tests.lcd import Lcd
from tests.encoder import Encoder

# aka new zapojeni sasci.
# CLK -> D1 (GPIO5)
# DT  -> D2 (GPIO4)
# SW  -> D3 (GPIO0)
encoder = Encoder(clk_pin=5, dt_pin=4, sw_pin=0)

# setupneme lcd. piny jsou napsane v nejakem md najdi si to 
display = Lcd()

# nastavime index scrollu na 0
# scroll index 0 - 2
index = 0



# tezsi na pochopeni, vytvorime stromovou strukturu, chatgpt kdyztak vysvetli
class Menu:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

# vytvorime main menu
main = Menu("Main")

# vytvorime sub menu
sub = Menu("Sub")

# vytvorime heat menu
heat = Menu("Heat")

# sub menu je child main menu
main.add_child(sub)
# heat menu je child sub menu
sub.add_child(heat)

# main>sub>heat ez jak facka to vis

# nastavime current menu na main
current = main  

# vstoupime do sub menu
current = current.children[0]

# vstoupime do heat menu
current = current.children[0]

# vratime se zpet jasny jak facka
current = current.parent

# ted jsme vyresili to, ze nemusime ukladat historii a proste objekt vi co je nad nim a pod nim.


# trosku down loop drz hubu 
while True:
    # nastavime click enkoderu na false
    click = False

    # nastavime c promena ktera me napadla pravepodobne change - abychom nevykreslovali v kazdem loopu screen, vykreslime ho pouze kdyz je zmena
    change = False
    
    # getneme rotace a click
    encoder_rotation = encoder.on_rotate()
    encoder_click = encoder.on_click()
    
    # vyhodnotime enkoder. 
    if encoder_rotation == 1:
        index = max(0, index - 1)
        change = True

    elif encoder_rotation == -1:
        index = min(2, index + 1)
        change = True


    if encoder_click == 1:
        # print("Click: Pressed")
        click = True
        change = True

    # pokud se neco zmenilo provedeme zmeny
    if change: 
        # clearneme display. nutne pokazde, postupne vykreslujeme veci - vrstvime je na sebe jako hamburger
        display.clear()
        # vykreslime sub menicko
        display.draw_sub_menu()
        # vykreslime arrows do menicka
        display.draw_menu_arrows()
        # vykreslime momentalni index co si nastavime v enkoderu
        display.draw_scroll(index)  
        # vykreslime heating bar
        display.draw_heating()
        # vse posleme do displaye a on si to vykresli
        display.show()