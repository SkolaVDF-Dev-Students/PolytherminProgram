"""
Hlavní program pro integraci enkodéru, ST7920 displeje a menu systému.
"""

import utime
from encoder import Encoder
from st7920_display import ST7920
from menu import Menu, create_test_menu

class MenuController:
    """
    Řadič propojující enkodér s menu systémem.
    """
    def __init__(self, encoder, menu):
        """
        Args:
            encoder: Instance Encoder třídy
            menu: Instance Menu třídy
        """
        self.encoder = encoder
        self.menu = menu
        self.long_press_threshold = 1000  # ms pro dlouhé stisknutí (návrat zpět)
        self.press_start_time = None
        
        # Registrovat callback funkce
        self.encoder.on_rotate(self.on_rotate)
        self.encoder.on_click(self.on_click)
    
    def on_rotate(self, direction):
        """
        Handler pro otáčení enkodéru.
        
        Args:
            direction: 1 = clockwise (scroll down), -1 = anticlockwise (scroll up)
        """
        if direction == 1:
            self.menu.scroll_down()
        else:
            self.menu.scroll_up()
        
        # Aktualizovat zobrazení
        self.menu.render()
    
    def on_click(self):
        """
        Handler pro stisk tlačítka enkodéru.
        """
        # Otevřít submenu nebo vykonat akci
        self.menu.select()
        self.menu.render()


def main():
    """
    Hlavní funkce programu.
    """
    print("Initializing system...")
    
    # Inicializace hardwaru
    # Enkodér: CLK=GPIO13, DT=GPIO12, SW=GPIO14
    encoder = Encoder(clk_pin=13, dt_pin=12, sw_pin=14)
    print("Encoder initialized")
    
    # Displej ST7920: CS=GPIO5, SID=GPIO4, CLK=GPIO0, RST=GPIO2
    display = ST7920(cs_pin=5, sid_pin=4, clk_pin=0, rst_pin=2)
    print("Display initialized")
    
    # Vytvoření menu
    test_items = create_test_menu()
    menu = Menu(display, test_items)
    print("Menu created")
    
    # Vytvoření řadiče
    controller = MenuController(encoder, menu)
    print("Controller initialized")
    
    # Počáteční vykreslení
    menu.render()
    print("System ready!")
    print()
    print("Controls:")
    print("  - Rotate encoder: Navigate menu")
    print("  - Middle click: Select / Open submenu")
    print()
    
    # Hlavní smyčka (držet program běžící)
    try:
        while True:
            utime.sleep(1)
    except KeyboardInterrupt:
        print("\nShutdown...")
        display.clear()
        display.update()


if __name__ == "__main__":
    main()
