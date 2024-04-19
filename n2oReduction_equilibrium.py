import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('TkAgg')

air = ct.Solution("gri30.yaml")
x0_n2o = 10000e-6
p = 15e5 # [Pa]
T_norm = 273  #[K]
T_min = 200+T_norm
T_max = 1500+T_norm
size = len(range(T_min,T_max))
x_n2o = np.zeros(size)
x_n2 = np.zeros(size)
x_no = np.zeros(size)
x_no2 = np.zeros(size)

for i,T in enumerate(range(T_min,T_max)):
    air.X = {"N2": 0.79 * (1 - x0_n2o), "O2": 0.21 * (1 - x0_n2o), "N2O": x0_n2o}
    air.TP = T, p
    air.equilibrate("TP")
    x_n2o[i] = air.X[air.species_index("N2O")]
    x_n2[i] = air.X[air.species_index("N2")]
    x_no2[i] = air.X[air.species_index("NO2")]
    x_no[i] = air.X[air.species_index("NO")]


fig, ax1 = plt.subplots()
plt.plot(range(T_min-T_norm,T_max-T_norm),x_n2o*1e6,label = "N2O")
plt.plot(range(T_min-T_norm,T_max-T_norm),x_no*1e6, label = "NO")
plt.plot(range(T_min-T_norm,T_max-T_norm),x_no2*1e6, label = "NO2")
plt.xlabel("Temperature [°C]")
plt.ylabel("[ppm]")
ax2 = ax1.twinx()
ax2.plot(range(T_min-T_norm,T_max-T_norm),x_n2*100,color = "grey", label = "N2")
ax2.set_ylabel("N2 [mol %]")
fig.legend()
plt.show()


