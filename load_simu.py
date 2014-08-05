import json
from glob import glob
import os.path as osp
import numpy as np
from pylab import *
PATH = osp.split(osp.abspath(__file__))[0]

class Simu(object):
    def plot(self, legend=[]):
        """
        plots the data and appends as legend the value of the desired params
        ex: plot('resolution', 'grid_size' ,'clear_aperture')
        """
        label = ','.join([str(self.params['id']) + '_%s='%arg + str(self.params[arg]) \
                          for arg in legend])
        plot(self.data[0], 2*np.pi*1e6/(44.+self.data[1]), '-o', label=label)
        
def load(id):
    data_name = glob(PATH + '/data/*%04i_*.csv'%id)[0]
    json_name = glob(PATH + '/data/*%04i_*.json'%id)[0]
    res = Simu()
    with open(json_name,'r') as f:
        res.params = json.load(f)['params']
        res.params['id'] = id
    res.data = np.loadtxt(data_name, delimiter=',')
    
    return res

ids = [13,14,16,17,11,12]
length_scans = [load(id) for id in ids]
for scan in length_scans:
    scan.plot(legend = ['resolution',
                        'roc_depth' ,
                        'CA_roc'])
#yscale('log')
xlabel('length (m)')
ylabel('expected finesse')
legend(loc='best')
show()
