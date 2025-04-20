import PIL
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from Gaussian_fit import *
from merge_tif_files import *
from tqdm import tqdm
import pandas as pd

def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

def gaussian_process_data(img,directory,shine_duration,img_str,p_guess,offset_max,bounds=[(),()],plot=True,timeplot=True,excel=True,semilogy=True,chi=True):
    '''
    NOTE: ONLY TAKES ALREADY MERGED FILE AS INPUT
    NOTE2: p_guess is estimated array of 5 FIXED PARAMS  (no amp & no offset): p_guess=[x0,y0,sigma_x,sigma_y,theta]
    NOTE3: offset_max need to really guess, but can put somewhat high value cos it's max value of offset allowable
    NOTE4: bounds=[(),()] uses the script's inbuilt 20% range by default
    NOTE5: shine duration is how long the laser shines for. Format is a float in seconds.
    
    gaussian_process takes one already merged tif image file (img), and then does several things:
    (1) finds brightest frame and finds amp_max & fixed params x0,y0,sigma_x,sigma_y,theta from it
    (2) (plot=True) plots brightest frame fit and then saves image of it
    (3) fits all frames of the merged img tif file to 2D a gaussian for entire image
    (4) extracts all 8 values of all 8 parameters used for fitting (A,B,C,x0,y0,sigma_x,sigma_y,theta) at diff tim
    (5) (timeplot=True) plots out how the parameters change with time w/ laser (t,laser_on,laser_off) and saves image of it
    (6) (excel=True) saves these data as a table to a xlsx file as the name of the file
    '''    
    ## *** SET DIRECTORIES FOR SAVING GRAPHS AND XLSX
    
#     mac = '/Users/michael/Desktop/MOT DATA/250321 expt 2 (P=35W for 5s)/'
#     windows = 'Z:\\Personnel\\Michael\\260321 expt 3 (P=15,23,30,35,40,45,50W)\\'
    f_path = directory
    
    ### (0) CHECKS!
    
    p_guess = p_guess*1 
    for i in range(len(p_guess)):
        if p_guess[i] == 0:
            print ('Error! Cannot have 0 values in p_guess')
    
    ### (1a) USE BRIGHTEST FRAME TO FIND FIXED ALL PARAMETERS [x0,y0,sigma_x,sigma_y,theta]
    
    amp_max = np.amax(img)  #NOTE! amp_max is brightest PIXEL across entire img file
    
    brightness = []
    for i in range(np.shape(img)[0]):
        frame_brightness = np.sum(img[i])
        brightness.append(frame_brightness)            
    brightest_frame = np.argmax(brightness)                                          #find frame no. where we get brightest intensity
    
    p_guess = p_guess*1                                                              #p_guess = [x0,y0,sigma_x,sigma_y,theta], all ESTIMATES
    amp_guess = amp_max*0.5          
    offset_guess = offset_max*0.5   
    
    p0_guess = [amp_guess] + p_guess + [offset_guess]                                #set guess array for fitting 
    
    if (bounds==[(),()]):                                                            #if never specify bounds...
        x0_g,y0_g,sigma_x_g,sigma_y_g,theta_g = p_guess   #_g means _guess            #extract 5 guess fixed params from p_guess just now
        b_wide = [(0,x0_g*0.8,y0_g*0.8,sigma_x_g*0.8,sigma_y_g*0.8,theta_g*0.8,0),
         (amp_max,x0_g*1.2,y0_g*1.2,sigma_x_g*1.2,sigma_y_g*1.2,theta_g*1.2,offset_max)]     #bounds are within 20% for fixed params 

    if plot==True:
        print('Plotting 2D Gaussian fit for brightest frame, frame %d' %brightest_frame)
       
    pOpt,pCov,chisquare,fig_bright = gaussian2DFit(img[brightest_frame],p0_guess,b_wide,plot=plot)      #plot=True plots figs for BRIGHTEST
    fig_bright.savefig(f_path+img_str+'_brightestframefit.png', dpi=300, bbox_inches='tight')
        
    x0,y0,sigma_x,sigma_y,theta,offset = pOpt[1:7]   ## set params as fixed for all gaussian fits later
        
    ### (2&3) CALCULATES ALL PARAMETERS FOR EACH INDIV FRAME (BY 2D GAUSSIAN FIT) ACROSS ALL FRAMES OF IMG  

    n = np.shape(img)[0] #total no. of frames

    A = [] #empty array to keep amplitude A across time t
    B = [] #empty array to keep offset B across time t
    C = [] #empty array to keep chisquare C across time t

    x0_t = [] #same for all other parameters (but not as impt as A,B,C), _t means timed series
    y0_t = []
    sigma_x_t = []
    sigma_y_t = []
    theta_t = []

    #amp&offset bound min is always 0
    amp_max = amp_max*1
    offset_max = offset_max*1
    b_narrow = [(0,x0*0.99,y0*0.99,sigma_x*0.99,sigma_y*0.99,theta*0.99,0),
         (amp_max,x0*1.01,y0*1.01,sigma_x*1.01,sigma_y*1.01,theta*1.01,offset_max)]        # bounds set v narrow now 1% range 

    #fit for all frames in img
    for i in tqdm(range(n)):
        frame = img[i]
        offset = offset*1  
        amp = (i+1)/n*amp_max                          # assume amp linear scale: assume first frame amplitude=0, max_amp @ brightest region
        p0 = [amp,x0,y0,sigma_x,sigma_y,theta,offset]  # use values obtained from previous sample fitting at brightest frame

        optimized = gaussian2DFit(frame,p0,b_narrow,plot=False)  #let's not plot out all frames..
        pOpt_t=optimized[0]
        pCov_t=optimized[1]
        chisquare_t=optimized[2]
        
        A.append(pOpt_t[0])
        B.append(pOpt_t[6])
        C.append(chisquare_t)
        x0_t.append(pOpt_t[1])
        y0_t.append(pOpt_t[2])
        sigma_x_t.append(pOpt_t[3])
        sigma_y_t.append(pOpt_t[4])
        theta_t.append(pOpt_t[5])
        
    ### (4) PLOT OUT GRAPHS

    if timeplot==True:
        x = np.linspace(1,n,n) #x-axis is frame no., e.g. from 1-501, later for graph drawing
        fps = 50
        frametime = 1000/fps
        t = x*(frametime)/1000 #convert x-axis to s, given fps=50

        laser = np.zeros(n)
        start = 350 #start time in ms. fixed across all
        shineduration = shine_duration *  1000 #convert input shine_duration in s to ms
        shinetime = shineduration+25-125 #shine duration in ms, 25 is offset of script, 125 is another offset
        end = start+shinetime
        laser[int(start/frametime):int((end)/frametime)] = amp_max/3 # laser on/off i.e. 0/1: laser starts at 350ms and is on for (X+25)ms

        plt.figure(figsize=(16,8))
        plt.plot(t,A,label='amplitude A')
        plt.plot(t,B,label='offset B')
        plt.plot(t,laser,label='laser on/off')
#         plt.plot(t,x0_t,label='xo (pixels)')
#         plt.plot(t,y0_t,label='yo (pixels)')
#         plt.plot(t,sigma_x_t,label='$\sigma_x$ (pixels)')
#         plt.plot(t,sigma_y_t,label='$\sigma_y$ (pixels)')
#         plt.plot(t,theta_t,label='$\Theta$ (rad)')
        plt.xlabel('Time [s]')
        plt.ylabel('Parameters')
        if semilogy==True:
            plt.yscale('log')
            plt.title('Semilogy axis')
        if chi==True:
            plt.plot(t[1:],C[1:],label='scaled $\chi$')
        plt.legend()
        
        ## auto save image
        plt.savefig(f_path+img_str+'_timeseries.png', dpi=300, bbox_inches='tight')
        
        plt.show()
            
    ### (5) EXPORT TO EXCEL

    if excel==True:
        ## convert array into a dataframe 
        data = [t,A,B,C,x0_t,y0_t,sigma_x_t,sigma_y_t,theta_t,laser]
        df = pd.DataFrame (data)
        df_T = df.T #transpose i.e. swap row and col
    
        ## save as xlsx file
        filepath = f_path + img_str + '_data.xlsx'
        column_headings = ['time [s]','amplitude A [au]','offset B [au]','$\chi$ [au]','x0','y0','sigma_x','sigma_y','theta','laser [0/1]']

        df_T.to_excel(filepath, header=column_headings,index=False)
        
    print("for brightest frame, \nx0:%.2f\n"%x0 ,"y0:%.2f\n"%y0 ,"sigma_x:%.2f\n"%sigma_x, "sigma_y:%.2f\n"%sigma_y, "theta:%.2f\n"%theta ,"offset:%.2f\n"%offset, "for full image, amp_max:%.2f\n"%amp_max)