import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------
# Calibration data - chamber 1 magnets
# 12/10/2022 - magnets only
# 1-3 axis (measured from front face of main coil holder not permanent magnet holder)
displacement13 = np.linspace(20, 120, 11) - 11.9
field131 = np.array([33, -67, -73, -55, -33, -8, 19, 41, 61, 75, 64])
# swapped probe to less sensitive since reaching range of previous probe
field132 = np.array([67, -53, -77, -60, -35, 6, 23, 42, 61, 68, 30])  # last 2 points gaussmeter froze so we reset
field133 = np.array([70, -57, -73, -57, -26, 3, 28, 47, 71, 73, 36])

# 2-4 axis
displacement24 = np.linspace(20, 120, 11) - 11.9
field241 = np.array([-82, 39, 74, 59, 38, 2, -23, -43, -60, -68, -8])
field242 = np.array([-18, 63, 68, 44, 23, -1, -28, -49, -67, -69, -14])
field243 = np.array([-58, 54, 62, 51, 24, 9, -15, -47, -65, -67, -2])
# field24av = np.mean([field241, field242, field243], axis=0)
# df24 = pd.DataFrame(np.transpose([displacement24, field241, field242, field243, field24av]), columns = ['position (mm)','field 1 (Gauss)','field 2 (Gauss)', 'field 3 (Gauss)', 'average field (Gauss)'])
# df24m = df24.melt('position (mm)', var_name='data label', value_name='field (Gauss)')


# 13/10/2022 - permanent magnets and coils (9 A)
# + to R1, - to R4 (expect subtraction)
# 1-3 axis
displacement13c1 = np.linspace(20, 120, 11) - 11.9
field13c11 = np.array([110, -48, -56, -41, -22, 1, 18, 42, 55, 57, 13])
field13c12 = np.array([79, -25, -54, -44, -28, -2, 19, 40, 58, 61, 1])
field13c13 = np.array([150, -50, -58, -41, -20, -4, 18, 35, 53, 59, -18])
# 2-4 axis
displacement24c1 = np.linspace(20, 120, 11) - 11.9
field24c11 = np.array([-69, 40, 56, 41, 15, -4, -22, -41, -45, -53, -2])
field24c12 = np.array([20, 63, 51, 26, 10, -11, -30, -49, -54, -35, 65])
field24c13 = np.array([0, 55, 49, 34, 12, -18, -34, -49, -56, -33, 44])

# 9A + to R4, - to R1 (expect addition)
# 1-3
displacement13c2 = np.linspace(20, 120, 11) - 11.9
field13c21 = np.array([60, -87, -86, -56, -19, 15, 29, 44, 71, 90, 65])
field13c22 = np.array([-25, -75, -80, -54, -25, -11, 24, 49, 76, 89, 59])
field13c23 = np.array([12, -80, -80, -54, -34, 4, 25, 43, 74, 82, 47])
# 2-4
displacement24c2 = np.linspace(20, 120, 11) - 11.9
field24c21 = np.array([10, 84, 83, 51, 23, -10, -36, -52, -74, -70, -10])
field24c22 = np.array([26, 83, 78, 42, 24, -15, -30, -68, -76, -62, -9])
field24c23 = np.array([20, 82, 75, 50, 24, -13, -31, -55, -68, -72, -10])


# 14/10/2022 - tuning with individual coils
# Magnets only
# 1-3 axis (measuring from 3, with an additional 1 mm offset to the permanent magnet front face)
displacement132 = np.linspace(20, 120, 11) - 12.9
field1321 = np.array([-160, 11, 71, 69, 52, 27, -2, -24, -47, -68, -74])
field1322 = np.array([-176, 18, 69, 69, 51, 29, 0, -23, -45, -66, -72])
field1323 = np.array([-161, -10, 59, 70, 52, 29, 0, -25, -43, -65, -73])
# 2-4 axis (measuring from 4, with an additional 1 mm offset to the permanent magnet front face)
displacement242 = np.linspace(20, 120, 11) - 12.9
field2421 = np.array([169, -13, -61, -65, -50, -27, 3, 20, 43, 63, 75])
field2422 = np.array([140, -45, -50, -68, -51, -30, 5, 16, 40, 62, 75])
field2423 = np.array([148, -20, -47, -67, -54, -31, 11, 17, 39, 61, 74])
# Unknown sign of data points around zero - remove these points
displacement242 = np.array([20, 30, 40, 50, 60, 70, 90, 100, 110, 120]) - 12.9
field2421 = np.array([169, -13, -61, -65, -50, -27, 20, 43, 63, 75])
field2422 = np.array([140, -45, -50, -68, -51, -30, 16, 40, 62, 75])
field2423 = np.array([148, -20, -47, -67, -54, -31, 17, 39, 61, 74])

# One coil at a time
# Coil 1 - 9 A, - to red, + to black
displacement132c1 = np.linspace(20, 120, 11) - 12.9
field132c11 = np.array([-150, -6, 64, 67, 47, 20, -7, -30, -56, -79, -86])
field132c12 = np.array([-150, -14, 58, 68, 50, 25, 4, -27, -54, -75, -85])
field132c13 = np.array([-130, -10, 69, 67, 50, 24, 2, -27, -57, -76, -86]) # note - unsure if second point is + or - although this won't affect fit
# Coil 3 - 9A, + to black, - to red
displacement132c2 = np.linspace(20, 120, 11) - 12.9
field132c21 = np.array([-112, 28, 83, 80, 59, 31, 4, -20, -46, -67, -68])
field132c22 = np.array([-90, 45, 85, 79, 55, 30, 2, -26, -49, -69, -68])
field132c23 = np.array([-115, 32, 83, 81, 58, 31, 5, -23, -45, -65, -70])
# Coil 2 - 9 A, + to red, - to black
displacement242c1 = np.linspace(30, 120, 10) - 12.9
field242c11 = np.array([2, -55, -65, -48, -28, -3, 19, 48, 71, 86])
field242c12 = np.array([11, -54, -65, -48, -26, -7, 21, 46, 71, 87])
field242c13 = np.array([35, -50, -64, -52, -30, -5, 21, 49, 70, 87])
# Coil 4 - 9 A, + to red, - to black
displacement242c2 = np.linspace(30, 120, 10) - 12.9
field242c21 = np.array([3, -59, -73, -59, -34, -13, 13, 37, 10, 74])
field242c22 = np.array([37, -52, -74, -62, -41, -16, 12, 36, 57, 74])
field242c23 = np.array([12, -69, -76, -60, -35, -12, 13, 37, 58, 74])


# ------------------
# Analysis functions

def create_data_frame(x_data, field_data1, field_data2, field_data3):
    df = pd.DataFrame(np.transpose([x_data, field_data1, field_data2, field_data3]),
                      columns=['position','field1','field2', 'field3'])
    df['fieldAvg'] = df.loc[:, df.columns != 'position'].mean(axis=1)
    return df


def set_plot_parameters():
    return


def plot_field_data(dataframe, dataframe2='', figure_title='', xrange='', yrange='', fit=False, fitRange='', labelPosition=(70,70), doublePlot=False, fitLabels=['',''], labelType=''):
    cmap1 = plt.cm.viridis
    plt.rcParams["font.family"] = "serif"
    plt.rcParams['font.sans-serif'] = ['Garamond']
    textColour = (0.2, 0.2, 0.2)
    if xrange:
        dataframe = dataframe.loc[(dataframe['position'].between(np.min(xrange), np.max(xrange), inclusive='both'))]
        if doublePlot:
            dataframe2 = dataframe2.loc[(dataframe2['position'].between(np.min(xrange), np.max(xrange), inclusive='both'))]
    fig, axes = plt.subplots()
    sizes = 40
    alphas = 0.4
    dataframe.plot(ax=axes, kind='scatter', x='position', y='field1', color=cmap1(70), alpha=alphas, s=sizes)
    dataframe.plot(ax=axes, kind='scatter', x='position', y='field2', color=cmap1(150), alpha=alphas, s=sizes)
    dataframe.plot(ax=axes, kind='scatter', x='position', y='field3', color=cmap1(220), alpha=alphas, s=sizes)

    if doublePlot:
        shapes2 = 's'
        cmap2 = plt.cm.magma
        dataframe2.plot(ax=axes, kind='scatter', x='position', y='field1', color=cmap2(70), alpha=alphas, s=sizes, marker=shapes2)
        dataframe2.plot(ax=axes, kind='scatter', x='position', y='field2', color=cmap2(150), alpha=alphas, s=sizes, marker=shapes2)
        dataframe2.plot(ax=axes, kind='scatter', x='position', y='field3', color=cmap2(220), alpha=alphas, s=sizes, marker=shapes2)

    if yrange:
        axes.set(ylim=yrange)
    if fit:
        plot_fit_data(dataframe, fitRange, cmap1, axes, labelPosition, textColour, label=fitLabels[0], lineStyle='--', lT=labelType)
        if doublePlot:
            offsetLabel = np.subtract(labelPosition,(0,15))
            plot_fit_data(dataframe2, fitRange, cmap2, axes, offsetLabel, textColour, label=fitLabels[1], lineStyle='-.', lT=labelType)

    axes.set_xlabel('Position (mm)', fontsize=10, color=textColour)
    axes.set_ylabel('Magnetic field (Gauss)', fontsize=10, color=textColour)
    axes.set_title(figure_title, weight='bold', color=textColour)
    axes.tick_params(colors=textColour)
    axes.tick_params(color=textColour, labelcolor=textColour, which='both')
    for spine in axes.spines.values():
        spine.set_edgecolor(textColour)

    plt.minorticks_on()
    axes.grid(True, which='major', alpha = 0.9)
    axes.grid(True, which='minor', linestyle='-', alpha=0.1)

    # axes.legend(fitLabels)

    fig.tight_layout()
    plt.show()


def fit_field_data(dataframe, xrange):
    dfred = dataframe.loc[(dataframe['position'].between(np.min(xrange), np.max(xrange), inclusive='both'))]
    dfm = dfred.melt('position', var_name='dataLabel', value_name='field')
    dfmred = dfm.loc[(dfm['dataLabel'] != 'fieldAvg')]

    fit = np.polyfit(dfmred['position'].values.flatten(), dfmred['field'].values.flatten(), 1, full=True)
    dataframe['fit'] = dataframe['position']
    # dataframe['residuals'] = dataframe['field']
    # dataframe['stError'] = dataframe['position']
    dataframe['fit'] = dataframe['position'].apply(lambda x: np.polyval(fit[0],x))
    # dataframe['residuals'] -= dataframe['fit']
    # dataframe['stError'] = np.sqrt(np.sum())
    # print(dataframe)
    print(fit)
    return fit, dataframe


def plot_fit_data(df, fr, cm, ax, lP, tC, lT='', label='', lineStyle='-'):
    fitting = fit_field_data(df, fr)
    fitdf = fitting[1]
    fitdfRed = fitdf.loc[fitdf['position'].between(np.min(fr), np.max(fr), inclusive='both')]
    fitdfRed.plot(ax=ax, kind='line', x='position', y='fit', color=cm(20), alpha=0.8, legend=None, style=lineStyle)
    if label:
        if lT=='fullFit':
            fitLabel = label + ' = {:.2f} x + '.format(fitting[0][0][0]) + ' {:.2f}'.format(fitting[0][0][1])
        else:
            fitLabel = label + ' = {:.2f} G/mm'.format(fitting[0][0][0])
    else:
        fitLabel = 'field gradient = {:.2f} G/mm'.format(fitting[0][0][0])
    textbox = ax.annotate(fitLabel, xy=lP,
                            backgroundcolor='1', alpha=1, color=tC)
    textbox.set_bbox(dict(facecolor='white', alpha=0.5, edgecolor='none'))


# ---------------------
# Analysis and plotting

data13 = create_data_frame(displacement13, field131, field132, field133)
plot_field_data(data13, xrange=[15,110], figure_title='1-3 axis, permanent magnets', fit=True, fitRange=[35,90], labelPosition=(25,70))

data24 = create_data_frame(displacement24, field241, field242, field243)
plot_field_data(data24, xrange=[15,110], figure_title='2-4 axis, permanent magnets', fit=True, fitRange=[35,90], labelPosition=(70,70))


data13c1 = create_data_frame(displacement13c1, field13c11, field13c12, field13c13)
data13c2 = create_data_frame(displacement13c2, field13c21, field13c22, field13c23)
plot_field_data(dataframe=data13c1, dataframe2=data13c2, xrange=[15,110], figure_title='1-3 axis, permanent magnets + 9 A', fit=True, fitRange=[35,80],
                labelPosition=(20,70), doublePlot=True, fitLabels=['field gradient - ','field gradient + '])

data24c1 = create_data_frame(displacement24c1, field24c11, field24c12, field24c13)
data24c2 = create_data_frame(displacement24c2, field24c21, field24c22, field24c23)
plot_field_data(dataframe=data24c1, dataframe2=data24c2, xrange=[15,110], figure_title='2-4 axis, permanent magnets + 9A', fit=True, fitRange=[35,80],
                labelPosition=(60,70), doublePlot=True, fitLabels=['field gradient - ','field gradient + '])


# 14/10/2022
data132 = create_data_frame(displacement132, field1321, field1322, field1323)
data132c1 = create_data_frame(displacement132c1, field132c11, field132c12, field132c13)
data132c2 = create_data_frame(displacement132c2, field132c21, field132c22, field132c23)
plot_field_data(data132, dataframe2=data132c1, xrange=[20,110], figure_title='1-3 axis - coil 1', fit=True, fitRange=[40,90], labelPosition=(62,60),
                doublePlot=True, labelType='fullFit', fitLabels=['field no coils (G) ', 'field coil 1 @ 9 A (G) '])
plot_field_data(data132, dataframe2=data132c2, xrange=[20,110], figure_title='1-3 axis - coil 3', fit=True, fitRange=[40,90], labelPosition=(62,60),
                doublePlot=True, labelType='fullFit', fitLabels=['field no coils (G) ', 'field coil 3 @ 9 A (G) '])

data242 = create_data_frame(displacement242, field2421, field2422, field2423)
data242c1 = create_data_frame(displacement242c1, field242c11, field242c12, field242c13)
data242c2 = create_data_frame(displacement242c2, field242c21, field242c22, field242c23)
plot_field_data(data242, dataframe2=data242c1, xrange=[20,110], figure_title='2-4 axis - coil 2', fit=True, fitRange=[40,90], labelPosition=(30,60),
                doublePlot=True, labelType='fullFit', fitLabels=['field no coils (G) ', 'field coil 2 @ 9 A (G)'])
plot_field_data(data242, dataframe2=data242c2, xrange=[20,110], figure_title='2-4 axis - coil 4', fit=True, fitRange=[40,90], labelPosition=(30,60),
                doublePlot=True, labelType='fullFit', fitLabels=['field no coils (G) ', 'field coil 4 @ 9 A (G) '])