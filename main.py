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


# trosku down loop drz hubu 
while True:
    # nastavime c promena ktera me napadla pravepodobne change - abychom nevykreslovali v kazdem loopu screen, vykreslime ho pouze kdyz je zmena
    c = False
    # getneme rotace a click
    rotation = encoder.on_rotate()
    click = encoder.on_click()
    
    # vyhodnotime enkoder. trosku down
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

    # pokud se neco zmenilo provedeme zmeny
    if c: 
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