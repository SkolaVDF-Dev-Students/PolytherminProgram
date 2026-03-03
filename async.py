import asyncio
from machine import Pin

led = Pin(2, Pin.OUT)  # jen příklad, můžeš místo toho kreslit boot screen

# "Boot screen" task
async def bootscreen_task():
    # tady zobrazíš logo, text, animaci atd.
    print("Bootscreen start")
    for i in range(10):
        led.value(1)
        await asyncio.sleep_ms(100)   # krátký sleep, aby se scheduler dostal k ostatním taskům
        led.value(0)
        await asyncio.sleep_ms(100)
    print("Bootscreen hotový")

# další task – např. blikání / inicializace / čekání na něco
async def other_task():
    while True:
        # dělej něco neblokujícího
        print("Jiná async činnost")
        await asyncio.sleep(1)

async def main():
    # spustíš bootscreen paralelně s dalším kódem
    asyncio.create_task(bootscreen_task())
    asyncio.create_task(other_task())

    # hlavní smyčka – může být i prázdná, jen aby loop běžel
    while True:
        await asyncio.sleep(1)

# start v main.py
asyncio.run(main())
