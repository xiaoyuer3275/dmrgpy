import numpy as np

from . import taskdmrg
from .mps import MPS

def random_mps_dummy(self,normalize=True):
    """Generate a random MPS, beware of a complicated statistial
    distribution"""
    task = {"random_mps":"true",
            }
    self.task = task
    self.execute( lambda : taskdmrg.write_tasks(self)) # write tasks
    self.execute( lambda : self.run()) # run calculation
    out = MPS(self,name="random.mps").copy() # copy
    norm = np.sqrt(out.overlap(out))
    return (1./norm)*out # return the eigenvector 






def random_product_state(self):
    """Generate a random product state, this ensures a correct
    statistical distribution of the generated states"""
    from .fermionchain import Fermionic_Chain
    from .spinchain import Spin_Chain
    mbc = self.clone() # clone the object
    mbc.maxm = 5
    mbc.nsweeps = 10
    h = 0 
    if type(mbc)==Fermionic_Chain: # fermionic chain
        for i in range(len(mbc.N)): # loop over sites
            if np.random.randint(2)==0: h = h + mbc.N[i] # empty
            else: h = h - mbc.N[i] # full
    elif type(mbc)==Spin_Chain: # spin chain
        for i in range(len(mbc.Sz)): # loop over sites
            m = np.random.random(3) -.5 # random magnetic field
            h = h + m[0]*mbc.Sx[i] + m[1]*mbc.Sy[i] + m[2]*mbc.Sz[i]  # empty
    else: raise # not implemented
    mbc.set_hamiltonian(h) # set the Hamiltonian
    wf = mbc.get_gs()
    wf.set_MBO(self)
    return wf


def random_mps(self):
    """Return a random MPS"""
    try: return random_product_state(self)
    except:
        print("Using the default routine")
        return random_mps_dummy(self)


