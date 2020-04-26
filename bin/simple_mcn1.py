from __future__ import print_function
from orphics import stats,io,mpi,maps,cosmology
from pixell import enmap
import numpy as np
import os,sys
import solenspipe
from falafel import qe
import mapsims
from enlib import bench
import healpy as hp
from solenspipe import bias


import argparse
# Parse command line
parser = argparse.ArgumentParser(description='Do a thing.')
parser.add_argument("label", type=str,help='Label.')
parser.add_argument("polcomb", type=str,help='polcomb.')
parser.add_argument("-N", "--nsims",     type=int,  default=10,help="Number of sims.")
parser.add_argument("--sindex",     type=int,  default=0,help="Declination band.")
parser.add_argument("--lmin",     type=int,  default=100,help="Minimum multipole.")
parser.add_argument("--lmax",     type=int,  default=3000,help="Minimum multipole.")
parser.add_argument("--isotropic", action='store_true',help='Isotropic sims.')
parser.add_argument("--no-atmosphere", action='store_true',help='Disable atmospheric noise.')
parser.add_argument("--use-cached-norm", action='store_false',help='Use  cached norm.')
parser.add_argument("--wnoise",     type=float,  default=None,help="Override white noise.")
parser.add_argument("--beam",     type=float,  default=None,help="Override beam.")
parser.add_argument("--disable-noise", action='store_true',help='Disable noise.')
parser.add_argument("--healpix", action='store_true',help='Use healpix.')
parser.add_argument("--no-mask", action='store_true',help='No mask. Use with the isotropic flag.')
parser.add_argument("--debug", action='store_true',help='Debug plots.')
parser.add_argument("--flat-sky-norm", action='store_true',help='Use flat-sky norm.')
args = parser.parse_args()

solint,ils,Als,Nl,comm,rank,my_tasks,sindex,debug_cmb,lmin,lmax,polcomb,nsims,channel,isostr = solenspipe.initialize_args(args)
      

w4 = solint.wfactor(4)
get_kmap = lambda seed: solint.get_kmap(channel,seed,lmin,lmax,filtered=True)
power = lambda x,y: hp.alm2cl(x,y)
qfunc = solint.qfunc

nmax = len(ils)

mcn1 = bias.mcn1(0,polcomb,polcomb,qfunc,get_kmap,comm,power,nsims,verbose=True)
mcn1[:nmax] = mcn1[:nmax] * Als[polcomb]**2. 
if not(args.no_mask):
    mcn1[:nmax] = mcn1[:nmax]/w4
    

mcn1[nmax:] = 0
io.save_cols(f'{solenspipe.opath}/n1_{polcomb}.txt',(ls,mcn1[:nmax]))


if rank==0:
    theory = cosmology.default_theory()
    
    ls = np.arange(rdn0.size)
    pl = io.Plotter('CL')
    pl.add(ls,mcn1)
    pl.add(ls,theory.gCl('kk',ls))
    #pl._ax.set_ylim(1e-9,1e-6)
    pl.done(f'{solenspipe.opath}/recon_mcn1.png')
                                                                                   

                                                                                

