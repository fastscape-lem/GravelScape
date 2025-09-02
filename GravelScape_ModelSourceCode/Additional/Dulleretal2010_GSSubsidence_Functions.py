import numpy as np
import xarray as xr
import xsimlab as xs

#Compute the 1D uplift and subsidence curve using a modified approach from Duller et al. (2010) for applications of the Fedele and Paola (2007) grain size fining solution
def SubsidenceCurve_Duller_BatchS0(alpha, u0, wm, wb, s0, x, ts, tf, ntime):
    import xarray as xr
    fact = (1 - np.exp(-alpha)) / alpha
    F = (u0 * wm) / (wb * fact * s0)
    ex = np.exp(-(x - wm) / wb * alpha)
    us = np.where(x<wm, 1, 0)
    u = np.where(x[np.newaxis,:,:]<wm, u0,-s0[:,np.newaxis,np.newaxis]*ex[np.newaxis,:,:])
    time = np.linspace(0,tf,ntime)
    u = xr.DataArray(u[:,np.newaxis,:, :] *np.where(time[np.newaxis,:,np.newaxis,np.newaxis]<ts, us[np.newaxis,np.newaxis,:,:], 1), dims=['F','time','y','x'])
    return u, F

def SubsidenceCurve_Duller_BatchF(alpha, u0, wm, wb, F, x, ts, tf, ntime):
    import xarray as xr
    fact = (1 - np.exp(-alpha))/alpha
    s0 = u0*wm/wb/fact/F
    ex=np.exp(-(x-wm)/wb*alpha)
    us = np.where(x<wm, 1, 0)
    u = np.where(x[np.newaxis,:,:]<wm, u0,-s0[:,np.newaxis,np.newaxis]*ex[np.newaxis,:,:])
    time = np.linspace(0,tf,ntime)
    u = xr.DataArray(u[:,np.newaxis,:, :] *np.where(time[np.newaxis,:,np.newaxis,np.newaxis]<ts, us[np.newaxis,np.newaxis,:,:], 1), dims=['F','time','y','x'])
    return u, F

def dullerGS(F, alpha, phi0, C1, CV, xstar): #computes grain size fining based on underlying subsidence conditions. 
    '''
    function to find mean grain size distribution along a channel profile subjected to subsidence and sedimentation (see Duller et al (2010))
    
    in Input:
    - F: ratio of sediment fluc into the system to sediment flux into the subsiding basin
      F=1: closed basin
      F<1: underfilled basin
      F>1: overspilling basin
    - alpha: controls the shape of the subsidence curve;
      subsidence decreases by a factor e^-alpha over the length of the basin
    - phi0: standard deviation in grainsize normalized by mean grain size (in source area)
    - C1: fining parameter
    - CV: coefficient of variation
    - xstar: array of normalized x-location where grain size should be computed (must be 0 and 1)
    
    in Output:
    - array of mean grain size normalized by source mean grain size at the xstar locations
    '''
    
    fact = 1-(1-np.exp(-alpha*xstar))/F/(1-np.exp(-alpha))
    #fact = np.where(fact>0, fact, np.nan)
    
    return 1+phi0/CV*(fact**C1-1)
