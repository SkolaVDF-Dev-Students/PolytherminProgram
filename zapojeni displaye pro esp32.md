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

D0-D7 (LCD datové piny) = NEPŘIPOJUJ (paralelní mód)
