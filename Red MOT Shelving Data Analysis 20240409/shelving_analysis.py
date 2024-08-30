import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks


class Shelving():
    """
    Implement the data analysis for the shelving measurements.

    Args:
        files (tuple): A tuple of the file names to be analyzed. The files should be 
        in csv format. The data should be in the following format:
        Time (s) , Channel A (mV)
        --       , --
    """

    def __init__(self, *files):

        self.files = files

    def extract_voltage_time(self):
        """Concatenate and return the voltage and time data from the files."""

        voltages = np.array([])
        times = np.array([])
        times_part = []
        for file in self.files:
            # Read and concatenate the data
            df = pd.read_csv(file)
            data = df.values
            voltages_part = np.array(data[1:, 1], dtype=float)

            # Make sure the time is increasing
            if times_part == []:
                times_part = np.array(data[1:, 0], dtype=float)
            else:
                times_part = np.array(
                    data[1:, 0], dtype=float) + times_part[-1]

            voltages = np.concatenate((voltages, voltages_part))
            times = np.concatenate((times, times_part))
        return voltages, times

    def plot_shelving_graph(self, figure_size=(10, 5), range=None):
        voltages, times = self.extract_voltage_time()

        plt.figure(figsize=figure_size)
        plt.plot(times, voltages)
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (mV)')
        plt.title('Shelving Graph')
        plt.show()

    def extract_peak_points(self, upper_border=200, lower_border=142, peak_distance=10000,
                            figure_size=(10, 5), time_intervals=[], plot=True):
        '''
        Return the array of the peak points we are interested in shelving measurements.

        Args:
            upper_border (int): The border line above which we consider the maximum peak. Ajust this to make sure 
                                we only get the peaks we are interested in. 
            lower_border (int): The border line below which we consider the minimum peak. Ajust this to make sure
                                we only get the peaks we are interested in.
            peak_distance (int): Required minimal horizontal distance (>= 1) in 
                                samples between neighbouring peaks.


        '''
        voltages, times = self.extract_voltage_time()

        indices_peaks_max = find_peaks(voltages, height=(upper_border, 10000),
                                       distance=peak_distance)[0]

        times_peaks_max = times[indices_peaks_max]
        voltages_peaks_max = voltages[indices_peaks_max]

        # Extract Minimum Peaks

        indices_peaks_min = find_peaks(-voltages, distance=peak_distance,
                                       height=(-lower_border, 0))[0]

        # Get the times and voltages at these indices
        times_peaks_min = times[indices_peaks_min]
        voltages_peaks_min = voltages[indices_peaks_min]

        # Plot the original data and the peaks
        if plot:
            plt.figure(figsize=figure_size)

            plt.plot(times, voltages)
            plt.plot(times_peaks_max, voltages_peaks_max, 'ro')
            plt.plot(times_peaks_min, voltages_peaks_min, 'bo')
        if len(time_intervals)!=0 and plot:
            # Plot the grouping lines
            for time in time_intervals:
                plt.axvline(x=time, color='r')
        if plot:
            plt.title('Shelving Sequence Auto Relock')
            plt.xlabel('Time (s)')
            plt.ylabel('Voltage (mV)')
            plt.show()

        return times_peaks_max, voltages_peaks_max, times_peaks_min, voltages_peaks_min

    def get_average_voltage(self, time_intervals, frequency_lists, plot=True):
        '''Return the grouped average voltages of the shelving measurements data.'''
        voltages, times = self.extract_voltage_time()

        # Group the voltages by time and calculate the average voltages
        df = pd.DataFrame(times, columns=['Time'])
        df['Voltage'] = voltages
        df['Interval'] = pd.cut(df['Time'], time_intervals)

        grouped = df.groupby('Interval')
        grouped_average_voltages = []
        grouped_times = []

        for interval, group in grouped:
            grouped_average_voltages.append(group['Voltage'].mean())
            grouped_times.append(group['Time'].to_numpy())

        grouped_average_voltages = np.array(grouped_average_voltages)

        average_voltages_by_frequency = {}
        for i in range(len(frequency_lists)):
            average_voltages_by_frequency[frequency_lists[i]] = \
                grouped_average_voltages[i]
        if plot:
            # plot the graph
            plt.figure(figsize=(10, 5))
            plt.plot(times, voltages)
            for i in range(len(time_intervals)-1):
                plt.hlines(y=grouped_average_voltages[i], xmin=time_intervals[i],
                           xmax=time_intervals[i+1],
                           color='r')

            plt.title('Average Sequence Auto Relock')
            plt.show()

        # return a dictionary with keys as the frequency and
        # values as the average voltages
        return average_voltages_by_frequency

    def get_shelving_amplitude(self, time_intervals, frequency_lists, method='subtraction',
                               error_bar=True, figure_size=(10, 5), plot=True,
                               upper_border=200, lower_border=142, peak_distance=10000,
                               normalised=False, plot_peak=True, plot_average=True):
        '''
        Return the average amplitudes and standard deviations of the shelving measurements data.

        Args:
            time_intervals (list): The list of time intervals to group the data. For example,
                                [0, 10, 20, 30] means the data will be grouped into 0-10s, 
                                10-20s, 20-30s.
            frequency_lists (list): The list of frequencies to group the data. For example,
                                [400, 600, 800] means the data will be grouped into 400THz, 600THz, 800THz.
            method (str): The method to calculate the average amplitudes. 
                        The default is 'subtraction'. Other options are 'max_to_average' 
                        and 'min_to_average'.
            error_bar (bool): If True, plot the graph with the error bar. The default is True.
            figure_size (tuple): The size of the figure. The default is (10, 5).
            plot (bool): If True, plot the graph. The default is True.
            upper_border (int): The border line above which we consider the maximum peak. 
            Ajust this to make sure we only get the peaks we are interested in.
            lower_border (int): The border line below which we consider the minimum peak. 
            Ajust this to make sure we only get the peaks we are interested in.
            normalised (bool): If True, normalise the amplitudes and standard deviations by the average voltage. 
            The default is False.
            plot_peak (bool): If True, plot the peaks extraction graph. The default is True.  
            plot_average (bool): If True, plot the average voltage graph. The default is True. 
        '''

        times_peaks_max, voltages_peaks_max, times_peaks_min, voltages_peaks_min = \
            self.extract_peak_points(upper_border=upper_border, lower_border=lower_border,
                                     peak_distance=peak_distance, time_intervals=time_intervals,
                                     plot=plot_peak)

        # Create dictionaries to store the max and min peaks
        max_peaks = {}
        min_peaks = {}

        for i in range(len(times_peaks_max)):
            max_peaks[times_peaks_max[i]] = voltages_peaks_max[i]

        for i in range(len(times_peaks_min)):
            min_peaks[times_peaks_min[i]] = voltages_peaks_min[i]

        # Group the max peaks by time
        df = pd.DataFrame(times_peaks_max, columns=['Time'])

        df['Interval'] = pd.cut(df['Time'], time_intervals)
        grouped_max = df.groupby('Interval')
        times_by_frequency_max = {}

        # Get the voltages for each interval
        # times_by_frequency_max is a dictionary with keys as the time intervals
        # and values as the times
        for interval, group in grouped_max:
            times_by_frequency_max[interval] = group['Time'].to_numpy()

        # Change the keys of the dictionary to the frequency
        i = 0
        keys = list(times_by_frequency_max.keys())
        for key in keys:
            times_by_frequency_max[frequency_lists[i]
                                   ] = times_by_frequency_max.pop(key)
            i += 1
        print("Grouping according to time for max peaks: ")
        print(times_by_frequency_max)

        # Group the min peaks by time
        df_min = pd.DataFrame(times_peaks_min, columns=['Time'])
        df_min['Interval'] = pd.cut(df_min['Time'], time_intervals)
        grouped_min = df_min.groupby('Interval')
        times_by_frequency_min = {}

        # Get the voltages for each interval
        for interval, group in grouped_min:
            times_by_frequency_min[interval] = group['Time'].to_numpy()

        i = 0
        keys = list(times_by_frequency_min.keys())
        for key in keys:
            times_by_frequency_min[frequency_lists[i]
                                   ] = times_by_frequency_min.pop(key)
            i += 1
        print("Grouping according to time for min peaks: ")
        print(times_by_frequency_min)

        # max_frequency_voltages is a dictionary with keys as the frequency and
        # values as the max voltages
        max_frequency_voltages = {}
        min_frequency_voltages = {}

        # Group the max and min voltages
        for frequency in frequency_lists:

            # max_peaks_times is the times of the max peaks for a certain frequency
            max_peaks_times = times_by_frequency_max[frequency]
            min_peaks_times = times_by_frequency_min[frequency]

            max_peaks_voltage = []
            for max_peaks_time in max_peaks_times:
                max_peaks_voltage.append(max_peaks[max_peaks_time])
            # max_peaks_voltage is the voltages of the max peaks for a certain frequency
            max_peaks_voltage = np.array(max_peaks_voltage)
            max_frequency_voltages[frequency] = max_peaks_voltage

            min_peaks_voltage = []
            for min_peaks_time in min_peaks_times:
                min_peaks_voltage.append(min_peaks[min_peaks_time])
            min_peaks_voltage = np.array(min_peaks_voltage)
            min_frequency_voltages[frequency] = min_peaks_voltage
        print("Grouping according to frequency for max peaks: ")
        print(max_frequency_voltages)
        print("Grouping according to frequency for min peaks: ")
        print(min_frequency_voltages)

        # Get the average voltages for each frequency
        average_grouped_voltages = self.get_average_voltage(
            time_intervals, frequency_lists, plot=plot_average)

        if method == 'subtraction':

            # Calculate the average amplitudes by directly averaging the half of the differences
            # between the max and min peaks
            shelving_amplitudes = []
            standard_deviations = []

            for frequency in frequency_lists:
                max_peaks_voltage = max_frequency_voltages[frequency]
                min_peaks_voltage = min_frequency_voltages[frequency]

                # Make sure the max and min peaks lists have the same length
                if len(max_peaks_voltage) != len(min_peaks_voltage):
                    if len(max_peaks_voltage) > len(min_peaks_voltage):
                        max_peaks_voltage = max_peaks_voltage[:len(
                            min_peaks_voltage)]
                    elif len(max_peaks_voltage) < len(min_peaks_voltage):
                        min_peaks_voltage = min_peaks_voltage[:len(
                            max_peaks_voltage)]

                # Make sure the list length is not zero
                if len(max_peaks_voltage) == 0:
                    average_amplitude = 0
                    standard_deviation = 0

                else:
                    average_amplitude = np.mean(
                        (max_peaks_voltage - min_peaks_voltage) / 2)
                    standard_deviation = np.std(
                        (max_peaks_voltage - min_peaks_voltage) / 2)
                shelving_amplitudes.append(average_amplitude)
                standard_deviations.append(standard_deviation)

            shelving_amplitudes = np.array(shelving_amplitudes)
            standard_deviations = np.array(standard_deviations)

        elif method == 'max_to_average':
            # Calculate the average amplitudes by taking the maximum peak and
            # subtracting the average of all the grouped voltage
            shelving_amplitudes = []
            standard_deviations = []

            for frequency in frequency_lists:
                max_peaks_voltage = max_frequency_voltages[frequency]
                average_voltage = average_grouped_voltages[frequency]
                max_average_amplitude = np.mean(
                    max_peaks_voltage - average_voltage)
                max_standard_deviation = np.std(
                    max_peaks_voltage - average_voltage)
                shelving_amplitudes.append(max_average_amplitude)
                standard_deviations.append(max_standard_deviation)

            shelving_amplitudes = np.array(shelving_amplitudes)
            standard_deviations = np.array(standard_deviations)

        elif method == 'min_to_average':
            shelving_amplitudes = []
            standard_deviations = []

            for frequency in frequency_lists:
                min_peaks_voltage = min_frequency_voltages[frequency]

                average_voltage = average_grouped_voltages[frequency]
                min_average_amplitude = np.mean(
                    average_voltage - min_peaks_voltage)
                standard_deviation = np.std(
                    average_voltage - min_peaks_voltage)
                shelving_amplitudes.append(min_average_amplitude)
                standard_deviations.append(standard_deviation)

            shelving_amplitudes = np.array(shelving_amplitudes)
            standard_deviations = np.array(standard_deviations)
        print(list(average_grouped_voltages.values()))
        print("Shelving Amplitudes and Standard Deviations: ")
        print(shelving_amplitudes)
        print(standard_deviations)
        if normalised:
            # Normalise the amplitudes and standard_deviations by the average voltage
            for i in range(len(shelving_amplitudes)):
                average_voltages = list(average_grouped_voltages.values())
                shelving_amplitudes[i] /= average_voltages[i]
                standard_deviations[i] /= average_voltages[i]

        if plot:
            if error_bar:
                # Plot the graph with the error bar
                plt.figure(figsize=figure_size)
                plt.errorbar(frequency_lists, shelving_amplitudes,
                             yerr=standard_deviations, fmt='o')
                plt.xlabel('Frequency (THz)')
                if normalised:
                    plt.title('Normalised Shelving Amplitude vs Frequency')
                    plt.ylabel('Amplitude Ratio(mV/mV)')
                else:
                    plt.title('Unnormalise Shelving Amplitude vs Frequency')
                    plt.ylabel('Amplitude (mV)')

            else:
                plt.figure(figsize=figure_size)
                plt.plot(frequency_lists, shelving_amplitudes, 'o')
                plt.xlabel('Frequency (MHz)')
                plt.ylabel('Amplitude (mV)')
                if normalised:
                    plt.title('Normalised Shelving Amplitude vs Frequency')
                    plt.ylabel('Amplitude Ratio(mV/mV)')
                else:
                    plt.title('Unnormalise Shelving Amplitude vs Frequency')
                    plt.ylabel('Amplitude (mV)')

        return shelving_amplitudes, standard_deviations

'''
file_1 = 'ShelvingSequenceAutoRelock\MirnyStart228MHz434829246THzEnd234MHzCSVs\MirnyStart228MHz434829246THzEnd234MHzCSVs_1.csv'
file_2 = 'ShelvingSequenceAutoRelock\MirnyStart228MHz434829246THzEnd234MHzCSVs\MirnyStart228MHz434829246THzEnd234MHzCSVs_2.csv'
file_3 = 'ShelvingSequenceAutoRelock\MirnyStart228MHz434829246THzEnd234MHzCSVs\MirnyStart228MHz434829246THzEnd234MHzCSVs_3.csv'
file_4 = 'ShelvingSequenceAutoRelock\MirnyStart228MHz434829246THzEnd234MHzCSVs\MirnyStart228MHz434829246THzEnd234MHzCSVs_4.csv'
file_5 = 'ShelvingSequenceAutoRelock\MirnyStart228MHz434829246THzEnd234MHzCSVs\MirnyStart228MHz434829246THzEnd234MHzCSVs_5.csv'

shelving_3 = Shelving(file_1, file_2, file_3, file_4, file_5)

# List of frequencies in MHz, corresponding to different groups of peaks
frequency_lists_3 = [228, 229, 230, 231, 232, 233]
# List of time intervals in seconds, corresponding to different groups of peaks
# with different frequencies. The intervals are as follows:
# 0-19, 19-30, 30-42, 42-50, 50-70
time_intervals = range(10, 77, 11)

average_voltages = shelving_3.get_average_voltage(
    time_intervals, frequency_lists_3)
print(average_voltages)

average_amplitudes_3, standard_deviations_3 = \
    shelving_3.get_shelving_amplitude(time_intervals,
                                      frequency_lists_3,
                                      upper_border=215,
                                      lower_border=130,
                                      method='min_to_average',
                                      error_bar=True,
                                      normalised=True
                               )
                               '''
