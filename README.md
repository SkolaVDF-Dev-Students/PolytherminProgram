# **Polythermin**
V tomto dokumentu je detailně popsáno elektro zapojení stroje a instalace programu. Nedoporučujeme cokoliv upravovat bez patřičných znalostí. 


# Instalace programu při sestavení stroje
- Ujistíme se že stroj je odpojený od elektrocké sítě a klíč je v poloze vypnuto.
 
1. Připojíme naše ESP32 k PC pomocí USB-C kabelu (Kabel musí být schopen přenášet data.).
2. Stáhneme si oficiální kód pro stroj na https://github.com/SkolaVDF-Dev-Students/PolytherminProgram/releases/
3. Pokud nemáme na našem PC python, nainstalujeme ho.
4. Nainstalujeme závislost pomocí pip: `pip install mpremote esptool`
5. Na desku nainstalujeme firmware, který si stáhneme na https://micropython.org/download/ESP32_GENERIC_S3/. Podrobný návod na jejich webu. Doporučujeme použít příkaz `python -m esptool --port {port} --baud 460800 write_flash 0 {firmware.bin}`
6. Poté co máme vše nainstalováno, spustíme tento příkaz a připojíme **náš aktualní adresář** k ESP32: `python -m mpremote mount .`
7. **Otestujeme zda vše funguje.**
8. Nahrajeme kompletní zdrojový kód pomocí: `mpremote connect auto fs cp -r . :`


# Testování a další vývoj kódu
- Kód si můžete přispůsobit podle licence
- Kód lze vyvíjet velice efektivně v jakémkoliv IDE


## Užitečné příkazy
- Smazaní aktuálních souborů a kódu - `python -m mpremote rm -r :/`
- Připojení našeho aktuální adresáře do ESP32 a vstup do REPLu -  `python -m mpremote mount .`
- Spuštění scriptu v REPLu  - `import main`
- Soft-reset REPLu (např. změna kódu, kód se neaktualizuje po uložení) - CTRL + D
- Exit kódu - CTRL + C
- Exit REPLu - CTRL + Q (VSC shortcut, blbý)


# Zapojení
## ENKODÉR
| Komponenta / Pin | ESP32-S3 Pin | GPIO | Jaký to má smysl? (Popis) |
| :--- | :--- | :--- | :--- |
| CLK (A) | IO4 | GPIO4 | Clock - točíš doprava/doleva |
| DT (B) | IO5 | GPIO5 | Data - točíš doprava/doleva |
| SW (Button) | IO6 | GPIO6 | Tlačítko |
| + (VCC) | 3.3V | - | Napájení |
| GND | GND | - | Zem (-) |0



## LCD (ST7920)
| Komponenta / Pin | ESP32-S3 Pin | GPIO | Jaký to má smysl? (Popis) |
| :--- | :--- | :--- | :--- |
| GND (VSS) | GND | - | Zem (-) |
| VCC (VDD) | 5V | - | Napájení (+) |
| V0 | Potenciometr | - | Kontrast (10kΩ zapojený mezi GND a 5V) |
| CS (RS) | IO11 | GPIO11 | SPI: CS / Slave Select |
| SID (R/W) | IO12 | GPIO12 | SPI: MOSI / Sériový data |
| CLK (E) | IO13 | GPIO13 | SPI: SCK / Hodiny |
| PSB | GND | - | SPI mód (MUSÍ bejt píchnuto do GND!) |
| NC | - | - | Nepřipojovat (fakt nesahej) |
| RST | IO14 | GPIO14 | Reset displeje |
| A (BLA) | 5V | - | Podsvícení anoda (+) |
| K (BLK) | GND | - | Podsvícení katoda (-) |

## Ostatní
| Komponenta / Pin | ESP32-S3 Pin | GPIO | Jaký to má smysl? (Popis) |
| :--- | :--- | :--- | :--- |
| Termistor 1 (T1) | IO15 | GPIO15 | Snímání teploty |
| Termistor 2 (T2) | IO16 | GPIO16 | Snímání teploty |
| Termistor 3 (T3) | IO17 | GPIO17 | Snímání teploty |
| LED indikace | IO1 | GPIO1 | Varovná kontrolka (> 70°C, ať si neopálíš pracky) |
| Relé topení | IO2 | GPIO2 | Spínání vyhřívání lisu (jestli to blafne, tvůj boj) |

## Zapojení ještě znovu
```text
                  +---------------------------+
                  |     ESP32-S3 N8R8 DEV     |
                  +---------------------------+
       (Enc VCC) -| 3V3                   GND |- (LCD_GND a BLK, Enc_GND, T_GND, IN_GND)
                  | 3V3                  IO43 |
                  | RST                  IO44 |
       (Enc CLK) -| IO4                   IO1 |- (LED)
        (Enc DT) -| IO5                   IO2 |- (Relé)
        (Enc SW) -| IO6                  IO42 |
                  | IO7                  IO41 |
   (Termistor 1) -| IO15                 IO40 |
   (Termistor 2) -| IO16                 IO39 |
   (Termistor 3) -| IO17                 IO38 |
                  | IO18                 IO37 |
                  | IO8                  IO36 |
                  | IO3                  IO35 |
                  | IO46                  IO0 |
                  | IO9                  IO45 |
                  | IO10                 IO48 |
        (LCD CS) -| IO11                 IO47 |
      (LCD MOSI) -| IO12                 IO21 |
       (LCD SCK) -| IO13                 IO20 |
       (LCD RST) -| IO14                 IO19 |
 (LCD_VCC, IN_5) -| 5V                    GND |
                  | GND                   GND |
                  +-----------+   +-----------+
                              |USB|
                              +---+
```

## Branches
| Název | Otestováno | Stabilní | Pozn. |
| :--- | :--- | :--- | :--- |
| main | ✅ | ✅ ||

- Ostatní stale jsou zastaralé archivní branche.