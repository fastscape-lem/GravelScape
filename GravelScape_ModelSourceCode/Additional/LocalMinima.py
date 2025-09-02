import numpy as np
import xarray as xr
import xsimlab as xs
import numba #for wrapping the function

#Calculates the slope between nodes within the drainage network where slopes that are zero or negative are set to zero (most likely local minima).
def find_slopes_withMinima (h, stack, rec,nrec):
    #This function computes the slope between each node and its receiver in multiflow
        #h : float #1D array containing landscape height
        #rec : int #1D array containing the list of receivers of each node. rec[ij] contains the list of receivers of ij.    
    nrec= np.where(nrec>0,nrec,0)
    #st= np.where(stack>0,stack,0)
    Slope=np.zeros_like(h) #!!! COPY
    for i in stack:
        r=rec[i,:]
        r=np.where(r>0,r,0)
        if r==i: #This is another way to avoid negative/undefined recievers
               continue
        temp=h[i]-h[r]
        if (any(temp <= 0)==1):
               Slope[i]=0
        else:
            Slope[i]=np.nanmean(temp)
    return Slope

#LocalMinima
#calc minima
#length=len(temp)
#@numba.njit
def TopoMin(TopoSlope2D,drain2D_P200):
    LocalMinFlag_2DP200=xr.DataArray(np.where(TopoSlope2D<=0,1,0).astype(float),dims=['out2','y','x'])
    TopoLong_1DP200=((LocalMinFlag_2DP200.sum('y')/(np.shape(LocalMinFlag_2DP200)[2])).sum('out2'))/(np.shape(LocalMinFlag_2DP200)[0])
#
    max_drainage_indices = xr.DataArray(drain2D_P200.argmax('y')).load()
    #max_drainage_indices = drain2D_P200.argmax('y')
    LocalMinChannel=np.zeros([len(TopoSlope2D.Precip),len(TopoSlope2D.y),len(TopoSlope2D.x)])
    #for f in range(np.shape(LocalMinFlag_2DP200)[0]):
    for o in range(np.shape(LocalMinFlag_2DP200)[0]):
        for p in range(np.shape(LocalMinFlag_2DP200)[-1]):
            LocalMinChannel[o,p]=(LocalMinFlag_2DP200.isel(out2=o).isel(x=p).sel(y=max_drainage_indices.values[f,o,p]))
    return LocalMinChannel


#calc slope
@numba.njit
def TopoSlope(Topo):
    DiffTopo=np.zeros_like(Topo)
    for f in range (np.shape(Topo)[0]):
        for t in range (np.shape(Topo)[1]): 
            for y in range (np.shape(Topo)[2]): 
                for x in range (np.shape(Topo)[3]): 
                    if x < np.shape(Topo)[3]-1:
                        DiffTopo[f,t,y,x]=Topo[f,t,y,x]-Topo[f,t,y,x+1]
    #DiffTopo=xr.DataArray(DiffTopo,dims=['F','Time','y','x'])
    return (DiffTopo)


#How to use it
#cellsize=1000
#TopoSlopeTemp=xr.DataArray(TopoSlope(zdataset.topography__elevation.isel(x=slice(1,202)).to_numpy()),dims=['time','y','x'])/cellsize#.mean('y').mean('out2')
#LocalMinChannel=xr.DataArray(TopoMin(TopoSlopeTemp,zdataset.drainage__flowacc),dims=["time",'out2','x'])
#G1F1BatchBeta_Minima=(LocalMinChannel.sum('out2')/len(zdataset.out2)).mean('x')