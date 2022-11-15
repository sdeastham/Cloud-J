#!/usr/bin/env python3

import numpy as np
from CloudJ import cloudj_python
import os

fjx_dir='Code.Cloud-J'
tables_dir=os.path.join(fjx_dir,'tables')

# All vectors are oriented with level 0 = surface
# If using a version of Cloud-J modified for GEOS input
#n_lev      = 72                        # Number of levels (hardcoded for now)
#n_cldlev   = 60                        # Number of levels which can contain cloud (also hardcoded)
# If using standard input
n_lev      = 57                        # Number of levels (hardcoded for now)
n_cldlev   = 34                        # Number of levels which can contain cloud (also hardcoded)
n_aer      = 2                         # Number of aerosol types (hardcoded for now)
U0         = 1.0                       # Cos(SZA)
PS_hPa     = 1013.25                   # Surface pressure, hPa
albedo     = np.zeros(5) + 0.05        # Albedo in 5 bands
wind       = 6.0                       # Surface wind in m/s - no idea why
chlr       = 0.08                      # Chlorophyll in mg/m3 - again, no idea
Ak_hPa     = np.zeros(n_lev+2)         # Ak in hPa at level edges
Bk         = np.zeros(n_lev+2)         # Bk at level edges (level 0 = surface)
T_K        = np.zeros(n_lev+2)         # Temperature at level edges
RH_frac    = np.zeros(n_lev+2)         # RH at level edges (0-1)
O3_ppbv    = np.zeros(n_lev+1)         # O3 v/v at level edges, ppbv
CH4_ppbv   = np.zeros(n_lev+1)         # CH4 v/v at level edges, ppbv
aerpath    = np.zeros((n_lev+2,n_aer)) # Aerosol path length at level edges, g/m2
aeridx     = np.zeros((n_lev+2,n_aer),np.int32)  # Aerosol types - 0=ignore, 1=bg strat sulf, 2=volc strat sulf
cld_frac   = np.zeros(n_cldlev)        # Cloud fraction in all levels
cld_lwc    = np.zeros(n_cldlev)        # Cloud liquid water content averaged over entire cell (g/g)
cld_iwc    = np.zeros(n_cldlev)        # Cloud ice water content averaged over entire cell (g/g)

# Use fixed pressure levels, varying exponentially from 1013.25 to ~3 hPa
Bk[:] = 0.0
for i_lev in range(n_lev+2):
    Ak_hPa[i_lev] = PS_hPa * np.exp(-i_lev/10)
T_K[:] = 280.0 # For now

# Set some representative values - force a fake ozone layer
O3_ppbv[np.logical_and(Ak_hPa[:-1] > 10.0, Ak_hPa[:-1] < 150.0)] = 1000.0
CH4_ppbv[:] = 1800.0

max_rates = 101 # JVN_ in Fast-JX
j_out = np.zeros((n_lev,max_rates))

#print(cloudj_python.run_cloudj.__doc__)

print('Initializing..')
cloudj_python.init_cloudj(tables_dir, True)

# The next two steps are for the user only - Cloud-J can be 
# run without doing these
print('Getting reaction count...')
n_rxn = cloudj_python.get_rxn_count()
print(f'{n_rxn} reactions identified. Reading reaction list...')
rxn_names = []
for i_rxn in range(n_rxn):
    i_out, rxn_out = cloudj_python.get_rxn(i_rxn)
    print(i_out,rxn_out)
    rxn_names.append(rxn_out.decode('utf-8'))
print('Reactions read. Starting Fast-JX runs..')
for sza in np.linspace(-np.pi,np.pi,11):
    U0 = np.cos(sza)
    # Output dimensions: [level, j-rate]
    j_out = cloudj_python.run_cloudj(tables_dir,U0,PS_hPa,albedo,wind,chlr,
                                     Ak_hPa,Bk,T_K,RH_frac,O3_ppbv,CH4_ppbv,
                                     aerpath[:,0],aeridx[:,0],aerpath[:,1],aeridx[:,1],
                                     cld_frac,cld_lwc,cld_iwc,n_lev,max_rates)
    max_idx = np.unravel_index(np.argmax(j_out),j_out.shape)
    i_lev_max = max_idx[0]
    i_j_max = max_idx[1]
    j_max = j_out[i_lev_max,i_j_max]
    j_max_name = rxn_names[i_j_max].strip()
    print(' --> SZA {:9.2f} deg: max J-rate {:8.2%} ({:s})'.format(sza*180.0/np.pi,j_max,j_max_name))
