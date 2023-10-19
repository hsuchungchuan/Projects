import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time as time

print('This script plots out parameters such as output power, wavelength, SolsTIS photodiode voltage, etc against pump power.')

print('Now Loading...')

plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 15
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['xtick.direction'] = 'out'
plt.rcParams['ytick.direction'] = 'out'
plt.rcParams['xtick.major.size'] = 5.0
plt.rcParams['xtick.minor.size'] = 3.0
plt.rcParams['ytick.major.size'] = 5.0
plt.rcParams['ytick.minor.size'] = 3.0
plt.rcParams['legend.handlelength'] = 1.0

filename = 'Z:/Shared/AION/Data/Msquared 689nm/msquared 689 characterization measurements.xlsx'
sheetname = input('Enter sheet name in excel file: ')
row_start = input('Enter row number where your data starts: ')
row_end = input('Enter row number where your data ends: ')

df = pd.read_excel(filename,sheet_name=sheetname,header=int(row_start)-2,nrows=int(row_end)-int(row_start)+1)

# # Power Curve
# 
# pumppower = df.iloc[:,0]
# highpower = df.iloc[:,4]
# lowpower = df.iloc[:,5]
#
# fig, ax1 = plt.subplots(figsize=(10,8))
# ax1.plot(pumppower,highpower,'bo',label='Output power')
# ax2 = ax1.twinx()
# ax2.plot(pumppower,lowpower,'ro',alpha=0.5,label='Fibre launch power')
#
# ax1.set_ylabel('Output power (high power PM) / W')
# ax1.set_xlabel('Pump power / W')
# ax2.set_ylabel('Fibre launch power (low power PM) / uW')
# datetime = time.strftime("%Y-%m-%d")
# plt.title('Power curve and fibre launch, ' + datetime)
# fig.legend(loc='upper left',bbox_to_anchor=(0.15,0.85))
# plt.show()
#


# Power + Wavelength

pumppower = df.iloc[:,0]
highpower = df.iloc[:,1]
wavelength = df.iloc[:,2]

fig, ax1 = plt.subplots(figsize=(10,8))
ax1.plot(pumppower,highpower,'bo',label='Output power')
ax2 = ax1.twinx()
ax2.plot(pumppower,wavelength,'ro',alpha=0.5,label='Wavelength')

ax1.set_ylabel('Output power (high power PM) / W')
ax1.set_xlabel('Pump power / W')
ax2.set_ylabel('Wavelength / nm')
datetime = time.strftime("%Y-%m-%d")
plt.title('Power curve and wavelength, ' + datetime)
fig.legend(loc='upper left',bbox_to_anchor=(0.15,0.85))
plt.show()

# Power Curve 2

pumppower = df.iloc[:,0]
highpower = df.iloc[:,1]
voltagepd = df.iloc[:,3]

fig, ax1 = plt.subplots(figsize=(10,8))
ax1.plot(pumppower,highpower,'bo',label='Output power')
ax2 = ax1.twinx()
ax2.plot(pumppower,voltagepd,'ro',alpha=0.5,label='PD voltage')

ax1.set_ylabel('Output power (high power PM) / W')
ax1.set_xlabel('Pump power / W')
ax2.set_ylabel('Solstis internal diode output PD / V')
datetime = time.strftime("%Y-%m-%d")
plt.title('Power curve and internal photodiode voltage, ' + datetime)
fig.legend(loc='upper left',bbox_to_anchor=(0.15,0.85))
plt.show()