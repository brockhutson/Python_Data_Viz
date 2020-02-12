# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 10:56:23 2019

@author: Brock

Week 1 practice project template for Python Data Visualization
Load a county-level PNG map of the USA and draw it using matplotlib

pylot. imread(), imshow(), show()
"""
    
    
import matplotlib.pyplot as plt

# Houston location

USA_SVG_SIZE = [555, 352]
HOUSTON_POS = [302, 280]

def draw_USA_map(map_name):
    """Given the name of a PNG map of the USA (specified as a string),
        draw this map using matplotlib
    """

     
    # Load map image, note that using 'rb'option in open() is critical since png files are binary
    with open(map_name, 'rb') as file:
        map_img = plt.imread(file)
#        print(filea)
        
    #  Get dimensions of USA map image
        ypixels, xpixels, bands = map_img.shape
        print(xpixels, ypixels, bands)
    
    # Plot USA map
        implot = plt.imshow(map_img)
        print(implot)
        
    # Plot green scatter point in center of map
        plt.scatter(x = xpixels / 2, 
                    y = ypixels / 2, 
                    s = 200, c='blue')
        
    # Plot red scatter point on Houston, Tx - include code that rescale coordinates for larger PNG files
        plt.scatter(x = HOUSTON_POS[0] * xpixels / USA_SVG_SIZE[0], 
                    y = HOUSTON_POS[1] * ypixels / USA_SVG_SIZE[1], 
                    s = 100, c = "Red")
        
#        plt.scatter(x = xpixels /2, 
#                    y = ypixels / 1, 
#                    s = 200, c='gold')
        
        plt.show()
draw_USA_map("USA_Counties_555x352.png")
draw_USA_map("USA_Counties_1000x634.png")   
