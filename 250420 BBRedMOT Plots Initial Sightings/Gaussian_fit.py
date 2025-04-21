import numpy as np
from scipy.optimize import curve_fit
from scipy.constants import *
import matplotlib.pyplot as plt
import matplotlib as mpl

def gaussian2D(X, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    '''
    Parameters:
        X: 2D array of data points
    '''
    x = X[0]
    y = X[1]
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = np.sin(2*theta)*(-1/(2*sigma_x**2) + 1/(2*sigma_y**2))
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
    g = offset + amplitude*np.exp(-(a*((x-xo)**2) + b*(x-xo)*(y-yo) + c*((y-yo)**2)))
    return g.ravel() #changes return output to 1D array

def gaussian2DFit(image, p0=None, bounds=[(), ()], plot=True):
    """
    Fits an image with a 2D gaussian.
    Parameters:
        image: numpy ndarray
        p0: ndarray, initial guess for the fit params in the form of
            [amplitude, xo, yo, sigma_x, sigma_y, theta, offset].
            Default None (fits for OD images).
        bounds: tuple of lower bound and upper bound for the fit.
            Default None (fits for OD images)
        plot:  bool to show the plot of the fit. Default True.
    Returns:
        pOpt: optimized parameters in the same order as p0
        pCov: covarience parameters of the fit.
        Read scipy.optimize.curve_fit for details.
    
    Curve_fit: use non-linear least squares to fit a function, f, to data.
    scipy.optimize.curve_fit(f, xdata, ydata, p0=None, sigma=None, bounds=- inf, inf)
    parameters:
        f: function e.g. formula
    """
    Ny, Nx = image.shape
    x = np.linspace(0, Nx, Nx, endpoint=False)
    y = np.linspace(0, Ny, Ny, endpoint=False)
    X = np.meshgrid(x, y) #2D array so shape is (2,x,y)
    
#     if (p0==None and bounds==[(),()]):  #if never input parameters, initial guess parameters that one usually sees; default settings
    p0 = [0.5, Nx/2, Ny/2, Nx/4, Ny/4, 0, 0]
    bounds = ([-0.5, 0.4*Nx, 0.4*Ny, 0.0*Nx, 0.0*Ny, -0.1, -0.5],\
            [10, 0.6*Nx, 0.6*Ny, 0.7*Nx, 0.7*Ny, 0.1, 1]) 

    pOpt, pCov = curve_fit(gaussian2D, X, image.reshape((Nx*Ny)), p0, bounds=bounds) #image.reshape((Nx*Ny)) converts to 1D array
    fit = gaussian2D(X, *pOpt).reshape(Ny, Nx) #"*" uses the entire pOpt parameter array, and .reshape(Ny,Nx) converts to 2D
    
    ## PLOTTING PARAMETERS
    
    if plot==True:
        f, ax = plt.subplots(nrows=1, ncols=6, gridspec_kw={'width_ratios': [5,5,5,0.2,5,0.2]}, figsize=(16, 4))
        
        ax[0].plot(image[int(pOpt[2])], 'r.') #pOpt[2] is y0 value, so we plot along y=y0 for different x values (horizontal)
        ax[0].plot(x, gaussian2D(np.meshgrid(x,int(pOpt[2])), *pOpt), 'k') #calculate brightness for (all x, y=y0) then plot against x
        ax[0].set_xlabel('x (pixels)')
        ax[0].set_ylabel('Fluorescence brightness (arbitrary units)')
        ax[0].set_title('Graph of brightness along \n x-axis horizontally at y=$\mathregular{y_0}$')
        
        ax[1].plot(image[:, int(pOpt[1])], 'r.')#pOpt[1] is x0 value, so plot along x=x0 for different y values (vertical)
        ax[1].plot(y, gaussian2D(np.meshgrid(int(pOpt[1]),y), *pOpt), 'k') #calculate brightness for (x=x0, all y) then plot against y
        ax[1].set_xlabel('y (pixels)')
        ax[1].set_ylabel('Fluorescence brightness (arbitrary units)')
        ax[1].set_title('Graph of brightness along \n y-axis vertically at x=$\mathregular{x_0}$')
        
#         if pOpt[0]<0.2:
#             ax[0].set_ylim(pOpt[6]-pOpt[0]*1.2, pOpt[6]+pOpt[0]*1.2)
#             ax[1].set_ylim(pOpt[6]-pOpt[0]*1.2, pOpt[6]+pOpt[0]*1.2)
        
        ax[2].contour(X[0], X[1], fit, cmap=plt.cm.jet)#, vmin=pOpt[6]-pOpt[0]*0.12, vmax=pOpt[-1]+abs(pOpt[0])*1.2) #plot contour fit lines
        picture=ax[2].imshow(image, cmap=plt.cm.jet)#, vmin=pOpt[6]-pOpt[0]*0.12, vmax=pOpt[-1]+abs(pOpt[0])*1.2) #plot picture image
        f.colorbar(picture, cax=ax[3]) #put color bar beside on the right
        ax[2].set_xlabel('x (pixels)')
        ax[2].set_ylabel('y (pixels)')
        ax[2].set_title('Contour fit lines \n overlapped with image')
       
        diff = image-fit
        residue = ax[4].imshow(diff, cmap=plt.cm.jet)
        ax[4].set_xlabel('x (pixels)')
        ax[4].set_ylabel('y (pixels)')
        ax[4].set_title('Residue plot of difference \n between image and contour fit')
        f.colorbar(residue, cax=ax[5]) #put color bar beside on the right
        # plt.tight_layout()
        fig = plt.gcf()        
        plt.show()
        
        chisquare = np.sum(image-fit)/np.sum(image)
#         chisquare = np.sum(np.absolute(image-fit))/2000
        
        return pOpt, pCov, chisquare, fig
        
    chisquare = np.sum(image-fit)/np.sum(image)
        
    return pOpt, pCov, chisquare