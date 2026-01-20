# Návod na zapojení ST7920 LCD displeje a rotačního enkodéru

## Přehled komponentů

### 1. ST7920 128x64 LCD Displej
- Grafický LCD s modrým podsvícením
- Rozlišení: 128 x 64 pixelů
- Napájení: 5V
- Režim: **Sériový (SPI)**

### 2. Rotační enkodér (KY-040 nebo podobný)
- 3 piny: CLK, DT, SW
- Napájení: 3.3V - 5V

### 3. Mikrokontrolér
- ESP8266, ESP32, nebo jiný MicroPython kompatibilní čip

---

## Zapojení ST7920 Displeje (Sériový režim)

### Nastavení displeje do sériového režimu

> [!IMPORTANT]
> Pro aktivaci sériového režimu MUSÍ být pin **PSB (pin 15)** připojen na **GND (0V)**!

### Tabulka připojení

| ST7920 Pin | Pin Název | Připojit na | Popis |
|------------|-----------|-------------|-------|
| 1 | VSS | GND | Zem (záporné napájení) |
| 2 | VDD | 5V | Kladné napájení |
| 3 | V0 | Potenciometr (10kΩ) | Kontrast (střední pin potenciometru, krajní piny na VDD a GND) |
| 4 | CS | GPIO 5 | Chip Select (výběr čipu) |
| 5 | SID | GPIO 4 | Serial Data (sériová data) |
| 6 | CLK | GPIO 0 | Serial Clock (sériové hodiny) |
| 7-14 | DB0-DB7 | - | **NEPOUŽÍVAT** (pouze v paralelním režimu) |
| 15 | PSB | **GND** | **DŮLEŽITÉ: Připojit na GND pro sériový režim!** |
| 16 | NC | - | Nepřipojeno |
| 17 | /RESET | GPIO 2 | Reset (volitelné, nebo připojit na VDD) |
| 18 | VOUT | - | Nepřipojeno |
| 19 | A | 5V přes rezistor 100Ω | Podsvícení + (kladné) |
| 20 | K | GND | Podsvícení - (záporné) |

### Poznámky k zapojení displeje

1. **Kontrast (V0):** Připojte 10kΩ potenciometr mezi VDD a GND, střední pin na V0. Otáčením nastavíte kontrast.

2. **PSB Pin:** Tento pin určuje režim komunikace:
   - PSB = HIGH (5V) → Paralelní režim
   - PSB = GND (0V) → **Sériový režim** ← Používáme tento!

3. **Reset pin:** Můžete připojit na GPIO 2 pro softwarový reset, nebo natrvalo připojit na VDD (5V).

4. **Podsvícení:** Doporučuji přidat 100Ω rezistor mezi 5V a pin 19 (A) pro ochranu LED podsvícení.

---

## Zapojení Rotačního Enkodéru

| Enkodér Pin | Připojit na | Popis |
|-------------|-------------|-------|
| CLK | GPIO 13 | Hodinový signál otáčení |
| DT | GPIO 12 | Datový signál otáčení |
| SW | GPIO 14 | Tlačítko (middle click) |
| + | 3.3V nebo 5V | Napájení |
| GND | GND | Zem |

### Poznámky k zapojení enkodéru

- Některé enkodéry mají vestavěné pull-up rezistory, jiné ne
- Kód používá interní pull-up rezistory mikrokontroléru
- Pokud enkodér nefunguje správně, zkuste přidat externí pull-up rezistory (10kΩ) na CLK, DT a SW piny

---

## Schéma zapojení

```
ESP8266/ESP32                    ST7920 LCD Display
┌─────────────┐                 ┌────────────────┐
│             │                 │                │
│ GPIO 5  ----├─────────────────┤ 4 (CS)         │
│ GPIO 4  ----├─────────────────┤ 5 (SID)        │
│ GPIO 0  ----├─────────────────┤ 6 (CLK)        │
│ GPIO 2  ----├─────────────────┤ 17 (RESET)     │
│             │                 │                │
│ 5V      ----├─────────────────┤ 2 (VDD)        │
│ GND     ----├─────┬───────────┤ 1 (VSS)        │
│             │     └───────────┤ 15 (PSB) !!!   │
│             │                 │ 20 (K)         │
│             │                 │                │
└─────────────┘                 └────────────────┘
                                         │
                                    [10kΩ POT]
                                    └─ 3 (V0)


ESP8266/ESP32                    Rotační Enkodér
┌─────────────┐                 ┌────────────────┐
│             │                 │                │
│ GPIO 13 ----├─────────────────┤ CLK            │
│ GPIO 12 ----├─────────────────┤ DT             │
│ GPIO 14 ----├─────────────────┤ SW             │
│             │                 │                │
│ 3.3V/5V ----├─────────────────┤ +              │
│ GND     ----├─────────────────┤ GND            │
│             │                 │                │
└─────────────┘                 └────────────────┘
```

---

## Kontrolní seznam před zapnutím

- [ ] PSB pin (15) je připojen na GND
- [ ] VDD (pin 2) je připojen na 5V
- [ ] VSS (pin 1) je připojen na GND
- [ ] CS, SID, CLK jsou připojeny na správné GPIO piny
- [ ] Potenciometr je správně zapojen pro nastavení kontrastu
- [ ] Enkodér je připojen na GPIO 13, 12, 14
- [ ] Všechna GND jsou společná (displej, enkodér, mikrokontrolér)

---

## Spuštění programu

1. Nahrajte všechny soubory do mikrokontroléru:
   - `encoder.py`
   - `st7920_display.py`
   - `menu.py`
   - `main.py`

2. Spusťte hlavní program:
```python
import main
```

3. Nebo nastavte `main.py` jako boot soubor pro automatické spuštění

---

## Řešení problémů

### Displej se nezobrazuje nic
- Zkontrolujte, že PSB (pin 15) je připojen na GND
- Nastavte kontrast pomocí potenciometru
- Ověřte správné napájení (5V na VDD)

### Displej zobrazuje náhodné znaky
- PSB pin pravděpodobně není na GND (je v paralelním režimu)
- Zkontrolujte zapojení SID a CLK pinů

### Enkodér nereaguje
- Zkontrolujte zapojení CLK a DT pinů
- Přidejte externí pull-up rezistory (10kΩ)
- Vyzkoušejte prohodit CLK a DT piny

### Menu se hýbe chaoticky
- Enkodér má špatný debouncing
- Zkuste snížit citlivost v kódu
- Přidejte kondenzátory (0.1µF) na CLK a DT piny

---

## Užitečné odkazy a informace

**Datová specifikace ST7920:**
- Napájení: 5V ±10%
- Provozní teplota: -20°C až +70°C
- Velikost pixelu: 0,48 x 0,48 mm
- Rozteč pixelů: 0,52 x 0,52 mm

**GPIO Summary:**
- GPIO 0, 2, 4, 5: ST7920 Display
- GPIO 12, 13, 14: Rotační enkodér
