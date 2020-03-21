# Add the root path of the dmrgpy library
import os ; import sys ; sys.path.append(os.getcwd()+'/../../src')

import numpy as np
import matplotlib.pyplot as plt
from dmrgpy import parafermionchain
n = 3
pc = parafermionchain.Parafermionic_Chain(n) # create the chain

h = 0
for i in range(n):
  for j in range(n):
      h = h + pc.N[i]*pc.N[j]*np.random.random()
      h = h + pc.Sig[i]*pc.Sig[j]*np.random.random()
      h = h + 1j*pc.Sig[i]*pc.Sigd[j]*np.random.random()
      h = h + pc.Tau[i]*pc.Tau[j]*np.random.random()
      h = h + 1j*pc.Tau[i]*pc.Taud[j]*np.random.random()

h = h + h.get_dagger() # Make the Hamiltonian Hermitian
pc.set_hamiltonian(h) # set the Hamiltonian
print(pc.gs_energy(mode="DMRG"))
print(pc.gs_energy(mode="ED"))

print(pc.get_excited(mode="ED",n=10))

name = (pc.Chi[1],pc.Chi[1])
(e1,d1) = pc.get_dynamical_correlator(name=name,mode="ED",submode="INV")
(e0,d0) = pc.get_dynamical_correlator(name=name,mode="DMRG")

plt.plot(e0,d0,color="red",label="DMRG")
plt.plot(e1,d1,color="blue",label="ED")
plt.legend()
plt.show()
