from machine import ADC
import math
import time


class Thermistor:
    def __init__(self, pin, r_fixed, r0, beta, t0):
        """
        Setup termistoru. 

        Args:
            pin (int): ADC pin, na kterém je připojen termistor.
            r_fixed (float): Hodnota pevného rezistoru (Ohm).
            r0 (float): Odpor termistoru při referenční teplotě T0 (Ohm).
            beta (float): Beta konstanta termistoru.
            t0 (float): Referenční teplota v Kelvinech (např. 298.15 K = 25 °C).
        """
        self.pin = ADC(pin) 
        self.r_fixed =  r_fixed
        self.r0 = r0
        self.beta = beta
        self.t0 = t0
    

    def readValue(self):
        """
        Načte teplotu z termistoru.

        Returns:
            float | None: Teplota ve stupních Celsia,
            nebo None pokud je ADC hodnota mimo platný rozsah.
        """
        adc_value = self.pin.read()

        if adc_value <= 0 or adc_value >= 1023:
            return 0
        
        R_ntc = self.r_fixed * (1023 - adc_value) / adc_value

        temp_kelvin = 1 / ((1 / self.t0) + (1 / self.beta) * math.log(R_ntc / self.r0))
        
        return temp_kelvin - 273.15
