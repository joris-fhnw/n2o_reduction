import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.use('TkAgg')

breite = np.arange(1,6,0.2)
winkel = [15,20,25,30]
size_b = len(breite)
size_w = len(winkel)
hohe = np.zeros([size_w,size_b])
for i in range(size_w):
    for o in range(size_b):
        hohe[i,o] = breite[o] * np.arcsin(winkel[i] * np.pi / 180)

    plt.plot(breite, hohe[i],label = f"{winkel[i]}°")

plt.legend()
plt.xlabel("Messer breite [cm]")
plt.ylabel("Messer höhe [cm] (zum Zentrum des Messer)")
plt.grid()
plt.show(block=True)