from pylab import *
from rtlsdr import *
from time import sleep  
import pandas as pd  
sdr = RtlSdr()    
# configure device
sdr.sample_rate = 2.048e6  
sdr.center_freq = 53e6     
sdr.gain = 20 




lightmeup = []
times = []
gdat = []
for i in range(40000):
    current = np.datetime64(datetime.datetime.now())
    samps = sdr.read_samples(32500*256)
    maxme =  np.abs(samps).max()
    meanme = np.abs(samps).mean()
    sdme = np.abs(samps).std()
    ts = pd.to_datetime(str(current))
    fmt = ts.strftime('%y%m%d_%H%M_%S')
    fname = fmt+'_'+ '{:.4f}'.format(maxme).replace('.','p') + '.npy'
    gdat.append({'time': current, 'max': maxme, 'mean': meanme, 'stddev': sdme})
    print(f"Muestra {i}" )
    if maxme > 0.45:
        lightmeup.append({'time': current, 'sig' : samps})
        np.save('event_'+fname, {'time': current, 'sig' : samps})
        print(fmt, ' ', maxme, ' ', meanme, ' ', sdme)