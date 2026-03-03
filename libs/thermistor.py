from machine import ADC, Pin
import network

class Pt1000:
    def __init__(self, pin_id, r_ref=989.0, offset=0.0, gain=1.0):
        """
        Inicializace senzoru Pt1000.
        :param pin_id: Číslo GPIO pinu (např. 1)
        :param r_ref: Hodnota referenčního rezistoru v Ohmech
        :param offset: Kalibrační posun (přičítá se k výsledku)
        :param gain: Kalibrační násobič (zesílení)
        """
        # Vypnutí Wi-Fi pro snížení šumu ADC
        network.WLAN(network.STA_IF).active(False)
        network.WLAN(network.AP_IF).active(False)

        self.adc = ADC(Pin(pin_id))
        self.adc.atten(ADC.ATTN_11DB)  # Rozsah 0-3.3V
        
        self.r_ref = r_ref
        self.offset = offset
        self.gain = gain

    def get_raw_data(self):
        """Vrátí surový průměr z 20 měření ADC."""
        raw_sum = 0
        for _ in range(20):
            raw_sum += self.adc.read()
        return raw_sum / 20

    def read(self):
        """Provede kompletní měření a vrátí kalibrovanou teplotu."""
        raw = self.get_raw_data()
        napeti = raw * 3.3 / 4095
        
        # Výpočet odporu
        if napeti < 3.29:
            r_pt1000 = self.r_ref * napeti / (3.3 - napeti)
        else:
            r_pt1000 = 9999.0  # Chyba senzoru
            
        # Výpočet teploty (Lineární aproximace)
        teplota_raw = (r_pt1000 - 1000.0) / 3.85
        
        # Aplikace kalibrace
        teplota_kalib = (self.gain * teplota_raw) + self.offset
        return round(teplota_kalib, 2)