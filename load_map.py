import numpy as np
from pylab import imshow, xlabel, ylabel, colorbar, figure, plot, legend
from numpy import isnan
from scipy.optimize import curve_fit
import pickle

class Map:
    def __init__(self, filename):
        if filename.endswith(".ASC"):
            with open(filename) as f:
                params = {}
                line = f.readline()
                while line!='DATA_VALUES\n':
                    values = line.split(':')
                    if len(values)==1:
                        values = line.split('=')
                    if len(values)==2:
                        val = values[1].strip()
                        try:
                            val = float(val)
                        except ValueError:
                            pass
                        params[values[0].strip()] = val
                    line = f.readline()
                            
                    
                """
                line = f.readline()
                a = []
                while(line!=""):
                    a.append(float(line))
                    line = f.readline()
                """
                data = np.loadtxt(f)
                data[data==params['BAD_PIXEL_VALUE']] = np.nan
                data = data.reshape((params['COLS'],params['ROWS']))
        else:
            with open(filename, 'rb') as file_:
                dic = pickle.load(file_)
            data = dic.pop('profile')
            data = data[1:-1, 1:-1]
            
            params = dic
            params["COLS"] = data.shape[0]
            params["ROWS"] = data.shape[1]
            params['XPIXEL'], params['YPIXEL'] = params['pixelCal']
            
                
        self.params = params
        self.data = data
    
    def plot(self):
        """
        This plots a 2D image of the map in a new figure
        """
        self.jai_ete_plotte = True
        figure()
        imshow(self.data, extent=[0,
                        self.params['XPIXEL']*self.params['COLS'],
                        0,
                        self.params['YPIXEL']*self.params['ROWS']])
        xlabel('x [$\mu$m]')
        ylabel('y [$\mu$m]')
        colorbar()

    def plot_cuts(self):
        index_flat = np.nanargmin(self.data)
        index_x = index_flat/self.params['COLS']
        index_y = index_flat%self.params['COLS']
        cut_x = self.data[index_x,:]
        cut_y = self.data[:,index_y]
        x = np.linspace(0,
                        self.params['XPIXEL']*self.params['COLS'],
                        self.params['COLS'])
        y = np.linspace(0,
                        self.params['YPIXEL']*self.params['ROWS'],
                        self.params['ROWS'])

        """
        for abcisse, ordonnee = ((x, cut_x), (y, cut_y)):
            mask = - isnan(ordonnee)
            ordonnee = ordonnee[mask]
            abcisse = abcisse[mask]
        """
        mask_x = - isnan(cut_x)
        mask_y = - isnan(cut_y)

        self.x = x[mask_x]
        self.y = y[mask_y]
        self.cut_x = cut_x[mask_x]
        self.cut_y = cut_y[mask_y]

        plot(self.x, self.cut_x, label='cut_x')
        plot(self.y, self.cut_y, label='cut_y')
        legend(loc='best')

    def exclude(self, xmin, xmax, ymin, ymax):
        self.data[xmin:xmax, ymin:ymax] = np.nan

    def fit(self):
        res, flag = curve_fit(gaussian, self.y, self.cut_y,[0.5, 0.4, 50, 120, 1e-3])
        plot(self.y, gaussian(self.y, *list(res)))
        self.res_y = res
        
        res, flag = curve_fit(gaussian, self.x, self.cut_x,[0.5, 0.4, 50, 120, 1e-3])
        plot(self.x, gaussian(self.x, *list(res)))
        self.res_x = res
        



        return self.res_x, self.res_y
        
def gaussian(x, depth, offset, w, x0, slope):
    return offset - depth*np.exp(-(x - x0)**2/w**2) + slope*x
        
    """
    @classmethod
    def change_coucox_u(cls):
        cls.coucou = 25 
    """
