import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
from scipy.signal import find_peaks

class ShelvingAnalysis:
    
    def __init__(self, file_path):
        # Initialize with the file path and load data
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.time = None
        self.mot_pd_voltage = None

    def extract_data(self):
        # Extract the data from the file using the file path stored in the instance
        self.time = self.data.iloc[1:, 0].astype(float).to_numpy()
        self.mot_pd_voltage = self.data.iloc[1:, 4].astype(float).rolling(window=100).mean().to_numpy() + 160 # 3D MOT Vertical PD offset voltage was -160mV
    
    def extract_ROI_peaks(self, plot=False):
        # Extract ROIs from the data
        # The ROIs are the regions of interest that we are interested in.
        # In this case, the ROIs are the peaks in the shelving

        # First we define the peaks
        self.index_average_mot_pd = 200000 #t=2s
        ROI1_left = int(3.5*5e4+100000) #t=3.5s
        ROI1_right = int(4*5e4+100000) #t=4s
        ROI2_left = int(5.5*5e4+100000) #t=5.5s
        ROI2_right = int(6*5e4+100000) #t=6s
        ROI3_left = int(7.5*5e4+100000) #t=7.5s
        ROI3_right = int(8*5e4+100000) #t=8s
        ROI4_left = int(9.5*5e4+100000) #t=9.5s
        ROI4_right = int(10*5e4+100000) #t=10s

        # Then we extract the peaks
        self.mot_pd_voltage_ROI1 = self.mot_pd_voltage[ROI1_left:ROI1_right]
        self.peaks1, _ = find_peaks(self.mot_pd_voltage_ROI1, distance=ROI1_right-ROI1_left)
        self.mot_pd_voltage_ROI2 = self.mot_pd_voltage[ROI2_left:ROI2_right]
        self.peaks2, _ = find_peaks(self.mot_pd_voltage_ROI2, distance=ROI2_right-ROI2_left)
        self.mot_pd_voltage_ROI3 = self.mot_pd_voltage[ROI3_left:ROI3_right]
        self.peaks3, _ = find_peaks(self.mot_pd_voltage_ROI3, distance=ROI3_right-ROI3_left)
        self.mot_pd_voltage_ROI4 = self.mot_pd_voltage[ROI4_left:ROI4_right]
        self.peaks4, _ = find_peaks(self.mot_pd_voltage_ROI4, distance=ROI4_right-ROI4_left)

        if plot == True:
            plt.figure(figsize=(20, 8))
            plt.plot(self.time, self.mot_pd_voltage)
            plt.axvline(x=self.time[self.index_average_mot_pd], color='k', linestyle='--')
            plt.axhline(y=self.mot_pd_voltage[200000], color='k', linestyle='--')
            plt.axvline(x=self.time[ROI1_left], color='r', linestyle='--')
            plt.axvline(x=self.time[ROI1_right], color='r', linestyle='--')
            plt.axvline(x=self.time[ROI2_left], color='g', linestyle='--')
            plt.axvline(x=self.time[ROI2_right], color='g', linestyle='--')
            plt.axvline(x=self.time[ROI3_left], color='b', linestyle='--')
            plt.axvline(x=self.time[ROI3_right], color='b', linestyle='--')
            plt.axvline(x=self.time[ROI4_left], color='m', linestyle='--')
            plt.axvline(x=self.time[ROI4_right], color='m', linestyle='--')
            plt.plot(self.time[self.peaks1+ROI1_left], self.mot_pd_voltage_ROI1[self.peaks1], "x", color='r', markersize=20)
            plt.plot(self.time[self.peaks2+ROI2_left], self.mot_pd_voltage_ROI2[self.peaks2], "x", color='g', markersize=20)
            plt.plot(self.time[self.peaks3+ROI3_left], self.mot_pd_voltage_ROI3[self.peaks3], "x", color='b', markersize=20)
            plt.plot(self.time[self.peaks4+ROI4_left], self.mot_pd_voltage_ROI4[self.peaks4], "x", color='m', markersize=20)

        return self.mot_pd_voltage_ROI1, self.peaks1, self.mot_pd_voltage_ROI2, self.peaks2, self.mot_pd_voltage_ROI3, self.peaks3, self.mot_pd_voltage_ROI4, self.peaks4

    def extract_shelving_intensity(self):

        shelving_intensity_1 = self.mot_pd_voltage_ROI1[self.peaks1]/self.mot_pd_voltage[self.index_average_mot_pd] - 1 
        shelving_intensity_2 = self.mot_pd_voltage_ROI2[self.peaks2]/self.mot_pd_voltage[self.index_average_mot_pd] - 1
        shelving_intensity_3 = self.mot_pd_voltage_ROI3[self.peaks3]/self.mot_pd_voltage[self.index_average_mot_pd] - 1
        shelving_intensity_4 = self.mot_pd_voltage_ROI4[self.peaks4]/self.mot_pd_voltage[self.index_average_mot_pd] - 1

        shelving_intensity_avg = np.mean([shelving_intensity_1, shelving_intensity_2, shelving_intensity_3, shelving_intensity_4])
        shelving_intensity_std = np.std([shelving_intensity_1, shelving_intensity_2, shelving_intensity_3, shelving_intensity_4])

        return shelving_intensity_avg, shelving_intensity_std