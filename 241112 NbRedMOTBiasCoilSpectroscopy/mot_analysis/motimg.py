import numpy as np
from scipy.optimize import curve_fit
from numpy import reshape


class MOTImaging:
    
    def __init__(self, img):
        self.img = img
        self.popt = None 
    
    def blur_img(self, sample_rate_x = 8, sample_rate_y = 8):
        """
        img: 2D numpy array
        sample_rate: int, must be common divider of the image dimensions

        Description
        This method takes an 2D image and blur the image by taking sample_rate * sample_rate blocks 
        then taking the average of the block. blurring the image.
        Note: Remember to multiply the result by the sample rate if using this before fitting a 2D gaussian.
        """
        img = np.array(self.img)
        self.sample_rate_x = sample_rate_x
        self.sample_rate_y = sample_rate_y
        
        imgdim = np.array([len(img[0])/sample_rate_x, len(img)/sample_rate_y])
        reshaped_image = img.reshape(int(imgdim[0]), int(sample_rate_x), int(imgdim[1]), int(sample_rate_y))
        blurred_image = reshaped_image.mean(axis=(1, 3))
        
        self.img = blurred_image
        return blurred_image

    def gaussian_2d(self, xy, A, x0, y0, sigma_x, sigma_y, theta=0, offset=0, if_blurr = True):
    
        x, y = xy
        a = (np.cos(theta)**2) / (2*sigma_x**2) + (np.sin(theta)**2) / (2*sigma_y**2)
        b = -(np.sin(2*theta)) / (4*sigma_x**2) + (np.sin(2*theta)) / (4*sigma_y**2)
        c = (np.sin(theta)**2) / (2*sigma_x**2) + (np.cos(theta)**2) / (2*sigma_y**2)
        return A * np.exp(-(a * ((x - x0)**2) + 2 * b * (x - x0) * (y - y0) + c * ((y - y0)**2))) + offset
        #return A * np.exp(-(a * ((x - x0)**2) + c * ((y - y0)**2))) + offset
    
    def fit_2d_gaussian(self, if_blurr = True):
        
        if if_blurr:
            self.blur_img()
        # Generate the x and y coordinate arrays
        data = self.img
        x, y = np.indices(data.shape)
        
        # Initial guess for the parameters
        initial_guess = (data.max(), data.shape[1] // 2, data.shape[0] // 2, data.shape[1] // 2, data.shape[0] // 2, 0, data.min())

        # Flatten the data and the coordinate arrays
        x = x.ravel()
        y = y.ravel()
        data = data.ravel()
        
        # Fit the Gaussian model to the data
        self.popt, _ = curve_fit(lambda xy, A, x0, y0, sigma_x, sigma_y, theta, offset: 
                            self.gaussian_2d(xy, A, x0, y0, sigma_x, sigma_y, theta, offset),
                            (x, y), data, p0=initial_guess, maxfev=100000)
        
        if if_blurr:
            self.popt[1] =self.popt[1]* self.sample_rate_x
            self.popt[2] =self.popt[2]* self.sample_rate_y
            self.popt[3] =self.popt[3]* self.sample_rate_x
            self.popt[4] =self.popt[4]* self.sample_rate_y
        
        return self.popt