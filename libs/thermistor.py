from machine import ADC, Pin
import math


class Thermistor:
    def __init__(self, pin_id, r_ref=1000.0, v_ref=3.25, offset=0.0, gain=1.0):

        self.adc = ADC(Pin(pin_id))
        self.adc.atten(ADC.ATTN_11DB)

        self.r_ref = r_ref
        self.v_ref = v_ref
        self.offset = offset
        self.gain = gain

    # -------------------------
    # stabilní ADC čtení
    # -------------------------
    def get_raw_data(self, samples=30):
        values = [self.adc.read() for _ in range(samples)]
        values.sort()

        # trimmed mean (odstraní šum)
        trimmed = values[5:-5]
        return sum(trimmed) / len(trimmed)

    # -------------------------
    # napětí -> odpor
    # -------------------------
    def voltage_to_resistance(self, v):

        if v <= 0.01 or v >= (self.v_ref - 0.01):
            return None

        return self.r_ref * v / (self.v_ref - v)

    # -------------------------
    # Pt1000 model (SW optimalizace)
    # -------------------------
    def resistance_to_temp(self, R):

        if R is None:
            return None

        # 0–100 °C (nejpřesnější oblast)
        if R < 1385:
            temp = (R - 1000.0) / 3.85
            return temp

        # 100–300 °C (aproximace pro stabilitu)
        # (empiricky laděné pro Pt1000)
        a = 1.2e-5
        b = 0.24
        c = -190

        temp = a * R * R + b * R + c
        return temp

    # -------------------------
    # hlavní funkce
    # -------------------------
    def read(self):

        raw = self.get_raw_data()
        voltage = raw * self.v_ref / 4095.0

        resistance = self.voltage_to_resistance(voltage)
        temp = self.resistance_to_temp(resistance)

        if temp is None:
            return None

        # kalibrace
        temp = (temp * self.gain) + self.offset

        return round(temp, 2)