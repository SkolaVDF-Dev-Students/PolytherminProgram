LCD pin | ESP8266 pin | GPIO   | Popis
--------|-------------|--------|------------------
1  GND  | GND         | -      | Zem
2  VCC  | 5V          | -      | Napájení
3  V0   | Potenciometr| -      | Kontrast (10kΩ mezi GND-5V)
4  RS   | D8          | GPIO15 | CS/Slave Select
5  R/W  | D7          | GPIO13 | MOSI/Data
6  E    | D5          | GPIO14 | SCK/Clock
15 PSB  | GND         | -      | SPI mód (MUSÍ být GND!)
16 NC   | -           | -      | Nepřipojuj
17 RST  | D0          | GPIO16 | Reset
19 BLA  | 3.3V        | -      | Podsvícení modrá
20 BLK  | GND         | -      | Podsvícení zem

D0-D7 (LCD datové piny) = NEPŘIPOJUJ (paralelní mód)
