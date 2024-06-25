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
p = 5e5  # [Pa]
T_0 = 1500  # [K] inlet temperature
T_norm = 273  # [K]
x0_n2o = 1000e-6  # N2O in Air  [mol/mol]

lam = 2

length = 3e-6  # *approximate* PFR length [m]
u_0 = .006  # inflow velocity [m/s]
area = 1.e-4  # cross-sectional area [m**2]

# Resolution: The PFR will be simulated by 'n_steps' time steps or by a chain
# of 'n_steps' stirred reactors.
n_steps = 2000

# Cantera Objects
air = ct.Solution("gri30.yaml")
gas = ct.Solution("gri30.yaml")
gasmix = ct.Solution("gri30.yaml")

# Mixing of gas and combustion air
gas.TPX = T_0, p, {"CH4": .45, "CO2": .55}
air.TPX = T_0, p, {"N2": 0.79 * (1 - x0_n2o), "O2": 0.21 * (1 - x0_n2o), "N2O": x0_n2o}

# Mixing of the gas and the combust air
q1 = ct.Quantity(gas, mass=1)
q2 = ct.Quantity(air, mass=gas_lmin(gas) * lam)
q1.constant = q2.constant = 'HP'
q3 = q1 + q2

# calculating the exhaust
X_gasmix = q3.X  # [mol/mol] Molanteile des Gas Luft gemisches
gasmix.TPX = T_0, p, X_gasmix

mass_flow_rate1 = u_0 * gasmix.density * area

# create a new reactor
r1 = ct.IdealGasConstPressureReactor(gasmix)
# create a reactor network for performing time integration
sim1 = ct.ReactorNet([r1])

# approximate a time step to achieve a similar resolution as in the next method
t_total = length / u_0
dt = t_total / n_steps
# define time, space, and other information vectors
t1 = (np.arange(n_steps) + 1) * dt
z1 = np.zeros_like(t1)
u1 = np.zeros_like(t1)
states1 = ct.SolutionArray(r1.thermo)
for n1, t_i in enumerate(t1):
    # perform time integration
    sim1.advance(t_i)
    # compute velocity and transform into space
    u1[n1] = mass_flow_rate1 / area / r1.thermo.density
    z1[n1] = z1[n1 - 1] + u1[n1] * dt
    states1.append(r1.thermo.state)

plt.figure()
plt.plot(z1, states1.T)
plt.xlabel('$z$ [m]')
plt.ylabel('$T$ [K]')
# plt.legend(loc=0)
plt.show(block=True)


plt.figure()
plt.plot(t1*1e3, states1.X[:, gasmix.species_index('N2O')]*1e6, label='N2O')
plt.plot(t1*1e3, states1.X[:, gasmix.species_index('NO')]*1e6, label='NO')
plt.xlabel('$t$ [ms]')
plt.ylabel('$X$ [ppm]')
plt.legend(loc=0)
plt.show(block=True)
# plt.savefig('pfr_XN2O_t.png')
