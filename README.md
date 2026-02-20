# Vstřikovací lis.
- Varovaní: tento kód není určen pro nikoho. Při programovaní se jelo solidní piko. Jsme rádi, že to funguje. Děkujeme.
- tu bude popis o stroji zeo

# Zapojení
## Enkoder
| Pin Enkodéru | ESP32-S3 Pin | GPIO | Popis |
| :--- | :--- | :--- | :--- |
| GND | GND | - | Zem |
| + (VCC) | 3.3V | - | Napájení (Pozor, nepoužívej 5V!) |
| CLK (A) | IO5 | GPIO5 | Clock |
| DT (B) | IO4 | GPIO4 | Data |
| SW (Button) | IO7 | GPIO7 | Tlačítko|

## LCD
LCD pin | ESP32-S3 pin| GPIO   | Popis
--------|-------------|--------|------------------
1  GND  | GND         | -      | Zem
2  VCC  | 5V          | -      | Napájení
3  V0   | Potenciometr| -      | Kontrast (10kΩ mezi GND-5V)
4  RS   | IO10        | GPIO10 | CS/Slave Select
5  R/W  | IO11        | GPIO11 | MOSI/Data
6  E    | IO12        | GPIO12 | SCK/Clock
15 PSB  | GND         | -      | SPI mód (MUSÍ být GND!)
16 NC   | -           | -      | Nepřipojuj
17 RST  | IO13        | GPIO13 | Reset
19 BLA  | 5V          | -      | Podsvícení modrá
20 BLK  | GND         | -      | Podsvícení zem

# Spuštění kódu
- Pokud máte stroj, **kód se vám spustí sám po zapojení stroje**. Pokud sestavujete stroj nebo jste vývojář, potřebujete mít nejdřive splněno několik náležitostí.

1. Otevřeme elektrobox a odpojíme ESP32 od napájení. 
2. Připojíme náše ESP32 k PC pomocí USB-C kabelu (Kabel musí být schopen přenášet data.).
3. Pokud nemáme na našem PC python, nainstalujeme ho.
4. Nainstalujeme mpremote pomocí pip: `pip install mpremote`
5. Poté co máme vše nainstalováno, spustíme tento příkaz a připojíme se k ESP32: `python -m mpremote mount .`

- Odtud už lze spustit kterýkoliv script. Např. spustíme main.py `import main`
