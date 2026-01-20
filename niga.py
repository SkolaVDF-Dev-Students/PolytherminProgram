from st7920_display import ST7920
d = ST7920(5, 4, 0, 2)
d.clear()
d.text("HELLO", 30, 28)
d.rect(0, 0, 128, 64, 1)
d.update()