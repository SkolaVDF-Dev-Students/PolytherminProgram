from st7920 import Screen

lcd = Screen()
lcd.clear()
plot = lcd.create_plotter()

size = 8

for row in range(0, 64 // size):
    for col in range(0, 128 // size):
        if (row + col) % 2 == 0:
            for x in range(col * size, (col+1) * size):
                for y in range(row * size, (row+1) * size):
                    plot(x, y)

lcd.redraw()
print("Šachovnice!")
