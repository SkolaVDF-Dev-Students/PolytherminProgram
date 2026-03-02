from machine import ADC, Pin
import time

# =====================================================
# KONFIGURACE - ZMĚŇ ZDE SVÉ HODNOTY
# =====================================================
adc = ADC(Pin(1))           # GPIO1 = ADC pin (změň na svůj pin, např. Pin(2))
adc.atten(ADC.ATTN_11DB)    # Rozsah 0-3.3V (nutné pro měření)

R_REF = 988.0               # TVŮJ REZISTOR 988 OHM - změřený multimetrem!

# KALIBRACE - uprav podle měření
# OFFSET: pokud kód ukazuje MÍŇ teplotu → ZVĚTŠI (+), VÍCE → ZMĚŇŠI (-)
OFFSET = 0.0                # Např. +2.3 nebo -1.5 podle testu

# GAIN: jen pokud chyba roste s teplotou (většinou 1.0 stačí)
GAIN = 1.0                  # Např. 0.98 pokud vysoké teploty jsou podceněné

print("PT1000 DEBUG s R_REF=988Ω")
print("Zapojení: 3V3 ─── 988Ω ─── GPIO1 ─── PT1000 ─── GND")
print("Kalibrace: změř termometrem, uprav OFFSET/GAIN výše")
print("Ctrl+C = stop\n")

try:
    while True:
        # ================================
        # MĚŘENÍ - průměr 20 hodnot pro stabilitu (méně šumu)
        # ================================
        raw_sum = 0
        for i in range(20):
            raw_sum += adc.read()  # 0-4095 (12bit)
        raw = raw_sum / 20
        print(f"DEBUG: RAW průměr={raw:.1f} z 20 měření")
        
        # ================================
        # VÝPOČET NAPĚTÍ
        # ================================
        napeti = raw * 3.3 / 4095
        print(f"      Napětí na ADC: {napeti:.3f} V")
        
        # ================================
        # VÝPOČET ODPO RU PT1000
        # Vzorec: R_pt1000 = R_REF * V_adc / (3.3 - V_adc)
        # ================================
        if napeti < 3.29:  # Bezpečnostní kontrola
            r_pt1000 = R_REF * napeti / (3.3 - napeti)
        else:
            r_pt1000 = 9999   # Chyba - senzor otevřený
        print(f"      Odpor PT1000: {r_pt1000:.1f} Ω (při 0°C=1000Ω)")
        
        # ================================
        # VÝPOČET TEPLOTY
        # Lineární: R = 1000 + 3.85 * T (°C) pro PT1000
        # T = (R - 1000) / 3.85
        # ================================
        teplota = (r_pt1000 - 1000.0) / 3.85
        teplota_kalib = GAIN * teplota + OFFSET
        
        # ================================
        # VÝPIS VŠECH HODNOT
        # ================================
        print(f"VÝSLEDEK: RAW:{raw:5.0f} V:{napeti:4.3f} R:{r_pt1000:6.1f} T:{teplota:6.2f}°C KALIB:{teplota_kalib:6.2f}°C")
        print("-" * 60)
        
        time.sleep(2)  # Měření každé 2 sekundy

except KeyboardInterrupt:
    print("\n=== UKONČENO ===")
    print("KALIBRACE:")
    print("1. Změř termometrem (např. pokoj 23°C)")
    print("2. Pokud KALIB ukazuje 21°C → OFFSET = +2.0")
    print("3. Restartuj kód")
    print("Očekávané: 25°C → R~1096Ω, RAW~2080")
