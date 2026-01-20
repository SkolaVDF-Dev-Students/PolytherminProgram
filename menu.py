class MenuItem:
    """
    Reprezentuje jednu položku v menu.
    """
    def __init__(self, text, submenu=None, action=None):
        """
        Args:
            text: Text zobrazený v menu
            submenu: Seznam dalších MenuItem pro submenu (volitelné)
            action: Funkce volaná při výběru (volitelné)
        """
        self.text = text
        self.submenu = submenu if submenu else []
        self.action = action
    
    def has_submenu(self):
        """
        Vrací True pokud má položka submenu.
        """
        return len(self.submenu) > 0


class Menu:
    """
    Správa menu s podporou scrollování a submenu.
    """
    def __init__(self, display, items):
        """
        Args:
            display: Instance ST7920 displeje
            items: Seznam MenuItem objektů
        """
        self.display = display
        self.root_items = items
        self.menu_stack = [items]  # Stack pro navigaci submenu
        self.selected_index = 0
        self.scroll_offset = 0
        self.items_per_screen = 8  # 64 pixels / 8 pixels per line
    
    def get_current_menu(self):
        """
        Vrací aktuální menu (top of stack).
        """
        return self.menu_stack[-1]
    
    def scroll_up(self):
        """
        Posune výběr nahoru.
        """
        current_menu = self.get_current_menu()
        if len(current_menu) == 0:
            return
        
        self.selected_index -= 1
        if self.selected_index < 0:
            self.selected_index = len(current_menu) - 1
        
        # Upravit scroll offset
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + self.items_per_screen:
            self.scroll_offset = self.selected_index - self.items_per_screen + 1
    
    def scroll_down(self):
        """
        Posune výběr dolů.
        """
        current_menu = self.get_current_menu()
        if len(current_menu) == 0:
            return
        
        self.selected_index += 1
        if self.selected_index >= len(current_menu):
            self.selected_index = 0
        
        # Upravit scroll offset
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = 0
        elif self.selected_index >= self.scroll_offset + self.items_per_screen:
            self.scroll_offset = self.selected_index - self.items_per_screen + 1
    
    def select(self):
        """
        Vybere aktuální položku (otevře submenu nebo zavolá akci).
        """
        current_menu = self.get_current_menu()
        if len(current_menu) == 0:
            return
        
        selected_item = current_menu[self.selected_index]
        
        if selected_item.has_submenu():
            # Otevřít submenu
            self.menu_stack.append(selected_item.submenu)
            self.selected_index = 0
            self.scroll_offset = 0
        elif selected_item.action:
            # Zavolat akci
            selected_item.action()
    
    def back(self):
        """
        Vrátí se o úroveň zpět v menu.
        """
        if len(self.menu_stack) > 1:
            self.menu_stack.pop()
            self.selected_index = 0
            self.scroll_offset = 0
    
    def render(self):
        """
        Vykreslí menu na displej.
        """
        self.display.clear()
        
        current_menu = self.get_current_menu()
        
        # Zobrazit položky
        visible_start = self.scroll_offset
        visible_end = min(visible_start + self.items_per_screen, len(current_menu))
        
        for i in range(visible_start, visible_end):
            y = (i - visible_start) * 8
            item = current_menu[i]
            
            # Text položky
            text = item.text
            if item.has_submenu():
                text = "> " + text  #Prefix pro submenu
            
            # Zkrátit text pokud je příliš dlouhý (max ~21 znaků pro 128px)
            if len(text) > 20:
                text = text[:17] + "..."
            
            self.display.text(text, 2, y)
            
            # Zvýraznit vybranou položku
            if i == self.selected_index:
                # Invertovat pozadí vybrané položky
                self.display.invert_rect(0, y, 128, 8)
        
        # Scrollbar indikátor (pokud je více položek než se vejde na obrazovku)
        if len(current_menu) > self.items_per_screen:
            # Vypočítat pozici a velikost scrollbaru
            scrollbar_height = max(8, (self.items_per_screen * 64) // len(current_menu))
            scrollbar_y = (self.scroll_offset * 64) // len(current_menu)
            
            # Nakreslit scrollbar na pravé straně
            self.display.vline(127, scrollbar_y, scrollbar_height)
        
        # Breadcrumb (indikátor hloubky menu)
        if len(self.menu_stack) > 1:
            depth_text = "< " + str(len(self.menu_stack) - 1)
            self.display.text(depth_text, 0, 56)
        
        self.display.update()


def create_test_menu():
    """
    Vytvoří testovací menu s 10 položkami a submenu.
    """
    menu_items = []
    
    for i in range(1, 11):
        # Submenu pro každou položku
        submenu = [
            MenuItem("Testing 1"),
            MenuItem("Testing 2"),
            MenuItem("Testing 3"),
            MenuItem("Testing 4"),
            MenuItem("Testing 5"),
        ]
        
        menu_items.append(MenuItem(f"Item {i}", submenu=submenu))
    
    return menu_items


if __name__ == "__main__":
    from st7920_display import ST7920
    
    # Inicializovat displej
    display = ST7920(cs_pin=5, sid_pin=4, clk_pin=0, rst_pin=2)
    
    # Vytvořit testovací menu
    items = create_test_menu()
    menu = Menu(display, items)
    
    # Vykreslit menu
    menu.render()
    
    print("Menu system initialized")
