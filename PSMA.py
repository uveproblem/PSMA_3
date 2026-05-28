from encodings import utf_8
import serial
import matplotlib.pyplot as plt
import numpy as np

urzadzenie = serial.Serial("/dev/tty.usbserial-A702SOBQ", 115200)

print(urzadzenie.readline())
lista = []
for i in range(300):
    try:
        dane = urzadzenie.readline().decode('utf-8').rstrip()
        danepodzielone = dane.split(',')
        pitch = float(danepodzielone[5])
        roll = float(danepodzielone[4])
        yaw = float(danepodzielone[6])
        lista.append((pitch, roll, yaw))
    except:
        print("Wyjebało błęda")

print(lista)
ypoint = np.array(lista)

plt.plot(ypoint, marker='o')
plt.show()