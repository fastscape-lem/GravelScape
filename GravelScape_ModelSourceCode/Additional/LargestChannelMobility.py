import numpy as np
import xarray as xr
import xsimlab as xs
import numba 

#drain2D = zdataset.drainage__flowacc #FastScape output for drainage
#THis code identifies anywhere the largest channel moves in space between two time steps
def largestchannel(Drainage):
    Binary=np.zeros_like(Drainage)
    DominantDrainage_YPath=Drainage.argmax('y',skipna=True).to_numpy()
    ChannelMobGrid=xr.DataArray(AvulsionMainChannel(Binary,DominantDrainage_YPath),dims=['time','y','x'])
    return ChannelMobGrid

# - Functions AvulsionMainChannel was designed for channels flowing in one direction from a orogenic source either in the x or y direction. 
# - In all the examples above, downstream from the orogenic front is along the x axis. 
# - Channels then migrate/avulse from their pathways along the y axis. 
# - AvulsionMainChannel takes 1)Binary: an empty (filled with zeros) array of the dimensions (eg (non-batch input with 3 dimensions): time, y, and x) of the Fastscape drainge output.
#     2) temp: the location of the dominant drainage pathway for each time step. 
# - AvulsionMainChannel can take batch inputs, but they need to be stacked as one batch input (eg: 4 dimensions). 
# - AvulsionMainChannel outputs a binary grid of where in the x and y the position of the channel changed between time steps (a mobility event).
# - In post processing, this can be summarized and divided by the time steps-1 in quesiton to derive a mobility frequency. 
def AvulsionMainChannel(Binary,temp):
    array=np.shape(Binary)
    if len(array)>=4:
        for a in range(np.shape(Binary)[0]):
            for b in range(np.shape(Binary)[1]):
                for d in range(np.shape(Binary)[3]):
                    Binary[a,b,temp[a,b,d],d]=1;
        AvulsionOccurance=np.zeros_like(Binary)
        for a in range(np.shape(Binary)[0]):
            for b in range(np.shape(Binary)[1]):
                for d in range(np.shape(Binary)[3]):                
                    if b != (np.shape(Binary)[1])-1:
                        #print(Binary[a,b,temp[a,b,d],d])
                        #print(Binary[a,b+1,temp[a,b,d],d])
                        #print('break')
                        AvulsionOccurance[a,b,temp[a,b,d],d]=int(Binary[a,b,temp[a,b,d],d] != Binary[a,b+1,temp[a,b,d],d])
        batchAvulse= AvulsionOccurance
    else:
                #for a in range(np.shape(Binary)[0]):
        for b in range(np.shape(Binary)[0]):
            for d in range(np.shape(Binary)[2]):
                Binary[b,temp[b,d],d]=1;
        AvulsionOccurance=np.zeros_like(Binary)
            #for a in range(np.shape(Binary)[0]):
        for b in range(np.shape(Binary)[0]):
            for d in range(np.shape(Binary)[2]):                
                if b != (np.shape(Binary)[0])-1:
                            #print(Binary[a,b,temp[a,b,d],d])
                            #print(Binary[a,b+1,temp[a,b,d],d])
                            #print('break')
                    AvulsionOccurance[b,temp[b,d],d]=int(Binary[b,temp[b,d],d] != Binary[b+1,temp[b,d],d])
        batchAvulse=  AvulsionOccurance 
    return batchAvulse

#Uses the grid of the movement of the largest channel to calculate a mobility frequency over time across the floodplain
def MobilityFrequency(Drainage,StartTime,EndTime):
    #BiChannels uses the output ChannelMobGrid that has 3 dimensions of time, y, and x.
    ChannelMovtGrid=largestchannel(Drainage)
    BiChannels=ChannelMovtGrid[StartTime:EndTime,:,:]
    #ThresholdQ=np.sum(DA,axis=0)*(ChannelThreshold);
    #BiChannels=np.where(DA>ThresholdQ,1,0); #This is an older version using a drainage threshold rather than the grid based on the largest channel
    size_BiChanTIME=len(BiChannels)
    AvulsionOccurance=np.zeros_like(BiChannels)
    for y in range(size_BiChanTIME-1):
        AvulsionOccurance[y,:]=(BiChannels[y,:] != BiChannels[y+1,:]).astype(int)
    AvulsionOverTime=np.sum(AvulsionOccurance,axis=0);
    AvulsionFrequency=xr.DataArray(AvulsionOverTime/(size_BiChanTIME-1),dims=['y','x']).max('y')
    return AvulsionFrequency