from machine import ADC, Pin

class Thermistor:
    def __init__(self, pin_id, r_ref=1000.0, v_ref=3.3):
        self.adc = ADC(Pin(pin_id))
        self.adc.atten(ADC.ATTN_11DB)
        self.r_ref = r_ref
        self.v_ref = v_ref

    def read(self):
        raw = self.adc.read()
        voltage = raw * self.v_ref / 4095.0

        if voltage <= 0 or voltage >= self.v_ref:
            return None
        R = self.r_ref * voltage / (self.v_ref - voltage)

        temp = (R - 1000.0) / 3.85

        return round(temp, 2)