## On your .ipynb, copy the plotting_style.py file to the same directory and add these to the .ipynb:

#import matplotlib.pyplot as plt
#from plotting_style import set_plotting_style
#set_plotting_style()

import matplotlib.pyplot as plt

print('Initialising plotting style...')

def set_plotting_style():
    plt.rc("font", family = 'Arial', size=10)
    plt.rc('axes', labelsize=20, titlesize = 20, labelpad=5)
    plt.rc('xtick', labelsize=18)
    plt.rc('ytick', labelsize=18)
    plt.rc('legend', fontsize=15)

print('Success! Plotting style initialised.')