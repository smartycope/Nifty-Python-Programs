from chempy import Equilibrium
from sympy import symbols
from chempy import Substance
'''
compound = Substance.from_formula(input("Enter first compound: "))
compound2 = Substance.from_formula(input("Enter second compound: "))

K1, K2, Kw = symbols('K1 K2 Kw')
e1 = Equilibrium(compound.composition, compound2.composition, K1)
e2 = Equilibrium({'O2': 1, 'H2O': 2, 'e-': 4}, {'OH-': 4}, K2)
coeff = Equilibrium.eliminate([e1, e2], 'e-')
redox = e1*coeff[0] + e2*coeff[1]
autoprot = Equilibrium({'H2O': 1}, {'H+': 1, 'OH-': 1}, Kw)
n = redox.cancel(autoprot)
redox2 = redox + n*autoprot
print(redox2)
'''

from chempy import balance_stoichiometry
reac, prod = balance_stoichiometry({'C7H5(NO2)3', 'NH4NO3'}, {'CO', 'H2O', 'N2'})
from pprint import pprint
# pprint(reac)
# {'C7H5(NO2)3': 2, 'NH4NO3': 7}
# >>> pprint(prod)
# {'CO': 14, 'H2O': 19, 'N2': 10}
from chempy import mass_fractions
for fractions in map(mass_fractions, [reac, prod]):
    pprint({k: '{0:.3g} wt%'.format(v*100) for k, v in fractions.items()})

# ferricyanide = Substance.from_formula('Fe(CN)6-3')
# print(ferricyanide.unicode_name)
# print('%.3f' % ferricyanide.mass)