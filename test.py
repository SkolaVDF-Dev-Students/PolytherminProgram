from machine import ADC, Pin
import math
import time

# --- KONFIGURACE ---
ADC_PIN = 4        # GPIO, kam máš zapojený střed děliče
R_REF = 1120        # Odpor tvého fixního rezistoru (změř ho multimetrem pro přesnost)
V_SYS = 3.3           # Napětí na 3V3 pinu ESP32
R0 = 1000.0           # 1000 pro Pt1000, 100 pro Pt100

class PtDiagnostic:
    def __init__(self, pin_id):
        self.adc = ADC(Pin(pin_id))
        self.adc.atten(ADC.ATTN_11DB)  # Rozsah do 3.3V
        self.adc.width(ADC.WIDTH_12BIT) # Rozlišení 0-4095

    def read_all(self):
        # 1. Čtení surového ADC (průměr z 50 vzorků pro stabilitu)
        raw_sum = 0
        for _ in range(50):
            raw_sum += self.adc.read()
        avg_raw = raw_sum / 50
        
        # 2. Převod na napětí (teoretické)
        v_out = (avg_raw / 4095.0) * V_SYS
        
        # 3. Výpočet odporu senzoru
        # Předpoklad: 3.3V -> R_REF -> ADC_PIN -> SENSOR -> GND
        if avg_raw >= 4090:
            res_status = "ROZPOJENO (Open Circuit)"
            resistance = float('inf')
        elif avg_raw <= 5:
            res_status = "ZKRAT (Short Circuit)"
            resistance = 0.0
        else:
            res_status = "OK"
            resistance = (v_out * R_REF) / (V_SYS - v_out)
        
        # 4. Výpočet teploty (Callendar-Van Dusen)
        A = 3.9083e-3
        B = -5.775e-7
        temp = -999
        if res_status == "OK":
            try:
                det = (A**2) - (4 * B * (1 - resistance / R0))
                temp = (-A + math.sqrt(det)) / (2 * B)
            except:
                temp = -998
                
        return avg_raw, v_out, resistance, res_status, temp

# Inicializace
diag = PtDiagnostic(ADC_PIN)

print("-" * 50)
print("DIAGNOSTIKA PT1000 / PT100")
print(f"Konfigurace: R_REF={R_REF} Ohm, R0={R0} Ohm")
print("-" * 50)

while True:
    raw, volt, res, status, temp = diag.read_all()
    
    print(f"ADC: {raw:>7.1f} | U: {volt:.3f}V | R_senzor: {res:>8.2f} Ohm | Stav: {status}")
    if status == "OK":
        print(f"   >>> VYPOČTENÁ TEPLOTA: {temp:.2f} °C <<<")
    print("-" * 50)
    
    time.sleep(2)