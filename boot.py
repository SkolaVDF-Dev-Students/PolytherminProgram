# tento kod se spusti jednou a to pri startu. nesmi loop!!!
# neotestovano!!!
import machine

from tests.thermistor import Thermistor
from tests.rele import Rele

# setup termistoru na GPIO 4, 5, 6
t1 = Thermistor(4, 100000, 100000, 3950, 298.15)
t2 = Thermistor(5, 100000, 100000, 3950, 298.15)
t3 = Thermistor(6, 100000, 100000, 3950, 298.15)

# nastavime relatko na pin 7
r = Rele(7)