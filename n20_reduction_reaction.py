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
