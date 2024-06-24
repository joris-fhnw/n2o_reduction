import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.use('TkAgg')


def gas_lmin(syngas):
    """
    Berechnet die Mindestluftmenge eines Gases in kg/kg
    :param syngas: Cantera Solution objekt
    :return: lmin [kg/kg]
    """
    omin = syngas.elemental_mass_fraction("C") * 2.664 + 7.937 * syngas.elemental_mass_fraction("H") + \
           - syngas.elemental_mass_fraction("O")
    lmin = omin / .2314
    return lmin


# Combust Properties
p = 1e5  # [Pa]
T = 300  #  [K]
T_norm = 273  #[K]
x0_n2o = 10000e-6  # N2O in Air  [mol/mol]

lam_min = 1.01
lam_max = 2.5
step = .01  # Auflösung
length = int(np.ceil((lam_max - lam_min) / step))  # Anzahl Berechnungsschritte
lam_vek = np.arange(lam_min, lam_max, step)

# Cantera Objects
air = ct.Solution("gri30.yaml")
gas = ct.Solution("gri30.yaml")
exhaust = ct.Solution("gri30.yaml")

# Initialize
x_n2o = np.zeros(length)
x_n2 = np.zeros(length)
x_no = np.zeros(length)
x_no2 = np.zeros(length)
T_vek = np.zeros(length)
x_o2 = np.zeros(length)


# Calculation of exhaust: equalize gas and air mixes with constant HP
for i, lam in enumerate(lam_vek):
    gas.TPX = T, p, {"CH4": .45, "CO2": .55}
    air.TPX = T, p, {"N2": 0.79 * (1 - x0_n2o), "O2": 0.21 * (1 - x0_n2o), "N2O": x0_n2o}

    # Mixing of the gas and the combust air
    q1 = ct.Quantity(gas, mass=1)
    q2 = ct.Quantity(air, mass=gas_lmin(gas) * lam)
    q1.constant = q2.constant = 'HP'
    q3 = q1 + q2

    # calculating the exhaust
    X_exhaust = q3.X  # [mol/mol] Molanteile des Gas Luft gemisches
    exhaust.TPX = T, p, X_exhaust
    exhaust.equilibrate("HP")  # Berechne das Gleichgewicht bei konstantem Druck und Temperatur

    x_n2o[i] = exhaust.X[exhaust.species_index("N2O")]
    x_n2[i] = exhaust.X[exhaust.species_index("N2")]
    x_no2[i] = air.X[exhaust.species_index("NO2")]
    x_no[i] = exhaust.X[exhaust.species_index("NO")]
    x_o2[i] = exhaust.X[exhaust.species_index("O2")]
    T_vek[i] = exhaust.T


# Plot

# fig = plt.Figure()
# ax1 = plt.subplots()
#
fig, ax1 = plt.subplots()
plt.plot(T_vek-T_norm, x_n2o * 1e6, label="N2O")
plt.plot(T_vek-T_norm, x_no * 1e6, label="NO")
plt.plot(T_vek-T_norm, x_no2 * 1e6, label="NO2")
plt.xlabel("T_ad [°C]")
plt.ylabel("[ppm]")
ax2 = ax1.twinx()
ax2.plot(T_vek-T_norm, x_o2 * 100, color="grey", label="O2")
ax2.set_ylabel("O2 [mol %]")
fig.legend()
plt.show(block=True)

