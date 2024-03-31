# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 10:50:16 2024

@author: Dell
"""

# %% Import packages
from analysis import *

#%% calculate velocitu and position from acceleration profile

def calculate_v_x(a, timestep):
    '''
    a: 1d array
    acceleration profile
    
    timestep: float
    time interval in s
    
    calculate velocity and position based on acceleration profile
    '''
    
    x = 0
    xarray = [0]
    
    v = 0
    varray = [0]
    
    for i in range(len(a)):
        v += a[i] * timestep
        varray.append(v)
        
        x += varray[i] * timestep
        xarray.append(x)
    return [varray[:len(a)],xarray[:len(a)]]

a = 5 * np.ones(10000)

tarr = np.linspace(0, 10, len(a))

velocity = calculate_v_x(a, 0.1)[0]
position = calculate_v_x(a, 0.1)[1]

plt.plot(tarr, position)

#%% accelaration ramp 

def a_minia(d, nos, timestep):
    tf = nos * timestep
    a0 = 4*d / tf**2
    a = []
    t = []
    temp = 0
    for i in range(nos):
        if i < nos/2:
            a.append(a0)
        else:
            a.append(-a0)
        temp = temp + timestep
        t.append(temp)
    return [t, a]

def x_minia(d, nos, timestep):
    tf = nos * timestep
    a0 = 4*d / tf**2
    x = []
    t = []
    temp = 0
    for i in range(nos):
        
        if i < nos/2:
            x.append(1/2 * a0 * temp**2)
        else:
            x.append(a0*tf*temp - 1/4*a0*tf**2 - 1/2*a0*temp**2)
        temp = temp + timestep
        t.append(temp)
    return [t, x]
plt.close()
at = a_minia(0.5,300,0.01)
position = calculate_v_x(at[1], 0.001)[1]
xt = x_minia(0.5,300,0.01)
plt.plot(xt[0], xt[1], linewidth = 5, label = 'Minimum acceleration')
#plt.plot(xt[0], position, '.', label = 'calculated')
plt.tick_params(axis='both', which='major', labelsize=18)
plt.xlabel('time (s)', fontsize=20,labelpad=5)
plt.ylabel('focus position (m)', fontsize=20,labelpad=5)
#plt.title('position - minimum acceleration ramp')
#plt.legend(fontsize=15, frameon=False)
plt.savefig('E://AtomECS_main//PyAtomECS//minia_x.pdf',bbox_inches='tight',dpi=300)

#%%


plt.plot(at[0], at[1], color = 'r', linewidth = 5, label = 'Minimum acceleration')
plt.tick_params(axis='both', which='major', labelsize=18)
plt.xlabel('time (s)', fontsize=20,labelpad=5)
plt.ylabel('acceleration (m/s$^2$)', fontsize=20,labelpad=5)
plt.savefig('E://AtomECS_main//PyAtomECS//minia_a.pdf',bbox_inches='tight',dpi=300)


#%% linear ramp
def x_linear(v, nos, timestep):
    tf = nos * timestep
    x = []
    t = []
    temp = 0
    for i in range(nos):
        x.append(v * temp)
        t.append(temp)
        temp = temp + timestep
    return [t, x]

xt = x_linear(0.5/3,300,3/300)
plt.plot(xt[0], xt[1], linewidth = 5, label = 'Minimum acceleration')
plt.tick_params(axis='both', which='major', labelsize=18)
plt.xlabel('time (s)', fontsize=20,labelpad=5)
plt.ylabel('focus position (m)', fontsize=20,labelpad=5)
plt.savefig('E://AtomECS_main//PyAtomECS//linear_x.pdf',bbox_inches='tight',dpi=300)

#%%

plt.plot(xt[0], np.zeros(300), color = 'r', linewidth = 5, label = 'Minimum acceleration')
plt.tick_params(axis='both', which='major', labelsize=18)
plt.xlabel('time (s)', fontsize=20,labelpad=5)
plt.ylabel('acceleration (m/s$^2$)', fontsize=20,labelpad=5)
plt.savefig('E://AtomECS_main//PyAtomECS//linear_a.pdf',bbox_inches='tight',dpi=300)

#%% Leonard ramp

def a_leonard(d, nos, timestep):
    tf = nos * timestep
    a0 = 6*d / tf**2
    a = []
    t = []
    temp = 0
    for i in range(nos):
        a.append(a0* (-2*temp/tf+1))
        temp = temp + timestep
        t.append(temp)
    return [t, a]

def x_leonard(d, nos, timestep):
    tf = nos * timestep
    a0 = 6*d / tf**2
    x = []
    t = []
    temp = 0
    for i in range(nos):
        x.append(1/2 * a0 * temp**2 - a0 * temp**3 /(3*tf))
        temp = temp + timestep
        t.append(temp)
    return [t, x]


at = a_leonard(0.5,300,0.01)
position = calculate_v_x(at[1], 0.001)[1]
xt = x_leonard(0.5,300,0.01)
plt.plot(xt[0], xt[1], linewidth = 5, label = 'Minimum acceleration')
plt.tick_params(axis='both', which='major', labelsize=18)
plt.xlabel('time (s)', fontsize=20,labelpad=5)
plt.ylabel('focus position (m)', fontsize=20,labelpad=5)
plt.savefig('E://AtomECS_main//PyAtomECS//leonard_x.pdf',bbox_inches='tight',dpi=300)

#%%
plt.close()
plt.plot(at[0], at[1], color = 'r', linewidth = 5, label = 'Minimum acceleration')
plt.tick_params(axis='both', which='major', labelsize=18)
plt.xlabel('time (s)', fontsize=20,labelpad=5)
plt.ylabel('acceleration (m/s$^2$)', fontsize=20,labelpad=5)
plt.savefig('E://AtomECS_main//PyAtomECS//leonard_a.pdf',bbox_inches='tight',dpi=300)


#%% Leonard ramp

def a_minijerk(d, nos, timestep):
    tf = nos * timestep
    a0 = 8*d / tf**2
    a = []
    t = []
    temp = 0
    for i in range(nos):
        if i < nos/4:
            a.append(4*a0/tf * temp)
        elif i < 3*nos/4:
            a.append(-4*a0/tf *(temp - tf/2))
        else:
            a.append(4*a0/tf * (temp - tf))
        temp = temp + timestep
        t.append(temp)
    return [t, a]

def x_minijerk(d, nos, timestep):
    tf = nos * timestep
    a0 = 8*d / tf**2
    x = []
    t = []
    temp = 0
    for i in range(nos):
        if i < nos/4:
            x.append(2/3*a0/tf * temp**3)
        elif i < 3*nos/4:
            x.append(a0/48 * (48*temp**2 - 32*temp**3/tf - 12*tf*temp + tf**2))
        else:
            x.append(a0 * (-2*temp**2 + 2*temp**3/(3*tf) + 2*tf*temp - 13/24 * tf**2))
        temp = temp + timestep
        t.append(temp)
    return [t, x]



at = a_minijerk(0.5,300,0.01)
position = calculate_v_x(at[1], 0.001)[1]
xt = x_minijerk(0.5,300,0.01)
plt.plot(xt[0], xt[1], linewidth = 5, label = 'Minimum acceleration')
plt.tick_params(axis='both', which='major', labelsize=18)
plt.xlabel('time (s)', fontsize=20,labelpad=5)
plt.ylabel('focus position (m)', fontsize=20,labelpad=5)
plt.savefig('E://AtomECS_main//PyAtomECS//minijerk_x.pdf',bbox_inches='tight',dpi=300)

#%%

plt.close()
plt.plot(at[0], at[1], color = 'r', linewidth = 5, label = 'Minimum acceleration')
plt.tick_params(axis='both', which='major', labelsize=18)
plt.xlabel('time (s)', fontsize=20,labelpad=5)
plt.ylabel('acceleration (m/s$^2$)', fontsize=20,labelpad=5)
plt.savefig('E://AtomECS_main//PyAtomECS//minijerk_a.pdf',bbox_inches='tight',dpi=300)

