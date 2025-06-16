# -*- coding: utf-8 -*-
"""
@author: Lea Gabele

Python code to analyze spine type frequency of your dendrite data. 
The code devides into filopodia, stubby, thin and mushroom spines and gives you the width of the respective spine type as well as your spine density.

Please be aware, that you need the following folder structure: condition --> round_x --> data (rois as .zip files)

IMPORTANT:  The width of each spine head should be the first roi in your roi.zip, the spine length the second and so on. 
            The length of the dendrite should be the last roi in your roi.zip.


"""

from tkinter import filedialog
import math
import os
import pandas as pd
import numpy as np
from read_roi import read_roi_zip

#################### Resolution ####################
"""
Please enter the resolution of your image, otherwise your data will be wrong!!!!!!!!!!
"""
global resolution #micron per pixel
#resolution = 0.1300000 # 63x Apo
resolution = 0.1018247 # Leica Images

#################### Functions ####################

def readRoiPuncta(roi_zip_path):
    # Create a list to store the result
    xy_pairs = []
    roi_list = []
    head_width_list = []
    spine_length_list = []
    #open the rois
    rois = read_roi_zip(roi_zip_path)

    for key, value in rois.items():
        xy_pairs = [[float(x), float(y)] for x, y in zip(value['x'], value['y'])]

        # Calculate the Euclidean distances between consecutive xy pairs within each ROI
        roi_distance = 0
        for j in range(len(xy_pairs) - 1):
            x1, y1 = xy_pairs[j]
            x2, y2 = xy_pairs[j + 1]
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            roi_distance += distance
        
        #get the correct values of microm
        roi_list.append(roi_distance*resolution)


    # Add values at odd indices (1st, 3rd, 5th, etc.) to list1
    head_width_list.extend(roi_list[0::2])
    
    # Add values at even indices (2nd, 4th, 6th, etc.) to list2
    spine_length_list.extend(roi_list[1::2])
    
    # Add the last value to last_values if it exists
    dendrit_length = roi_list[-1]
    print("Dendrite length: ", dendrit_length)
    
    #count the number of spines within the dendrite
    spine_count = len(head_width_list)
    
    #calculate spine density
    spine_density = (spine_count-1)/dendrit_length
    print("Spine density: ", spine_density)
    
    return dendrit_length, head_width_list, spine_length_list, spine_count, spine_density


#calculates the given spine type
def spineType(filename, roi_path):
    #path = os.path.join(data_path,roi_dat)
    spine_type_list = []
    
    #initialize variables to count spine types
    filopodia = 0
    mushroom = 0
    stubby = 0
    thin = 0
    
    #initinalize lists to calculate diameters per spine type
    filopodia_diameter = []
    mushroom_diameter = []
    stubby_diameter = []
    thin_diameter = []
    
    filopodia_length = []
    mushroom_length = []
    stubby_length = []
    thin_length = []
    
    dendrit_length, head_width_list, spine_length_list, spine_count, spine_density = readRoiPuncta(roi_path)
    
    for i in range(0, spine_count-1):
        head_diameter = head_width_list[i]
        spine_length = spine_length_list[i]

        if spine_length > 2 or ((head_diameter/spine_length)<0.25 
                                and spine_length > 1.5):
            spine_type_list.append("Filopodia")
            filopodia += 1
            filopodia_diameter.append(head_diameter)
            filopodia_length.append(spine_length)
            #print("Filopodia")
        elif head_diameter > 0.6:
            spine_type_list.append("Mushroom")
            mushroom += 1
            mushroom_diameter.append(head_diameter)
            mushroom_length.append(spine_length)
            #print("Mushroom")
        elif spine_length/head_diameter < 1 and spine_length < 1:
            spine_type_list.append("Stubby")
            stubby += 1
            stubby_diameter.append(head_diameter)
            stubby_length.append(spine_length)
            #print("Stubby")
        elif spine_length < 2:
            spine_type_list.append("Thin")
            thin += 1
            thin_diameter.append(head_diameter)
            thin_length.append(spine_length)
            #print("Thin")
        else:
            spine_type_list.append("Unknown")
    
    
    return  dendrit_length, np.mean(head_width_list), np.mean(spine_length_list), (spine_count-1), spine_density, filopodia, mushroom, stubby, thin, \
            np.mean(filopodia_diameter), np.mean(mushroom_diameter), np.mean(stubby_diameter), np.mean(thin_diameter), \
            np.mean(filopodia_length), np.mean(mushroom_length), np.mean(stubby_length), np.mean(thin_length)
    
#################### MAIN ####################

#get the path of your data
root_path = filedialog.askdirectory(title="Please select your folder of the condition to analyse.")

#get the path for your individual rounds
for round_folder in os.listdir(root_path):
    if round_folder == "Analysis":
        continue
    data_path = os.path.join(root_path, round_folder)
    results_path = os.path.join(root_path,"Analysis")
    if not os.path.exists(results_path):
        os.makedirs(results_path)
    
    #initialize dictionary for overall spine data
    spine_data = {
            'dendrite' : [],
            'spine_count' : [],
            'dendrite_length' : [],
            'spine_density' : [],
            'diameter' : [],
            'spine_length' : [],
        }
        
    #initialize your spine types dictionary to fill in later 
    spineTypes = {"filopodia", "stubby", "thin", "mushroom"}
    
    #initialize dictioinary of wanted analysis results per round
    spine_type_data = {}
    for spine_type in spineTypes:
        spine_type_data[spine_type] = {
            'dendrite': [],
            'count': [],
            'diameter': [],
            'spine_length' : [],
            'spine_type_density': [],
            'frequency': [],
        }   
    
    #get the path of each roi.zip to calculate the parameters for each dendrite
    for roi in os.listdir(data_path):
        if roi.endswith(".zip"):
            print(roi)
            roi_path = os.path.join(data_path, roi)
            dendrit_length, head_diameter, spine_length, spine_count, spine_density, filopodia, mushroom, stubby, thin, filopodia_diameter, mushroom_diameter, stubby_diameter, thin_diameter, filopodia_length, mushroom_length, stubby_length, thin_length = spineType(roi, roi_path)
            
            #fill your dictinoaries for overall spine data
            spine_data['dendrite'].append(roi)
            spine_data['spine_count'].append(spine_count)
            spine_data['dendrite_length'].append(dendrit_length)
            spine_data['spine_density'].append(spine_density)
            spine_data['diameter'].append(head_diameter)
            spine_data['spine_length'].append(spine_length)
            
            #fill your dictionaries for spine type data
            spine_type_data["filopodia"]["dendrite"].append(roi)
            spine_type_data["filopodia"]["count"].append(filopodia)
            spine_type_data["filopodia"]["diameter"].append(filopodia_diameter)
            spine_type_data["filopodia"]["spine_length"].append(filopodia_length)
            spine_type_data["filopodia"]["spine_type_density"].append(filopodia/dendrit_length)
            spine_type_data["filopodia"]["frequency"].append((filopodia/spine_count)*100)
            
            #fill your dictionaries for spine type data
            spine_type_data["mushroom"]["dendrite"].append(roi)
            spine_type_data["mushroom"]["count"].append(mushroom)
            spine_type_data["mushroom"]["diameter"].append(mushroom_diameter)
            spine_type_data["mushroom"]["spine_length"].append(mushroom_length)
            spine_type_data["mushroom"]["spine_type_density"].append(mushroom/dendrit_length)
            spine_type_data["mushroom"]["frequency"].append((mushroom/spine_count)*100)
            
            #fill your dictionaries for spine type data
            spine_type_data["stubby"]["dendrite"].append(roi)
            spine_type_data["stubby"]["count"].append(stubby)
            spine_type_data["stubby"]["diameter"].append(stubby_diameter)
            spine_type_data["stubby"]["spine_length"].append(stubby_length)
            spine_type_data["stubby"]["spine_type_density"].append(stubby/dendrit_length)
            spine_type_data["stubby"]["frequency"].append((stubby/spine_count)*100)
            
            #fill your dictionaries for spine type data
            spine_type_data["thin"]["dendrite"].append(roi)
            spine_type_data["thin"]["count"].append(thin)
            spine_type_data["thin"]["diameter"].append(thin_diameter)
            spine_type_data["thin"]["spine_length"].append(thin_length)
            spine_type_data["thin"]["spine_type_density"].append(thin/dendrit_length)
            spine_type_data["thin"]["frequency"].append((thin/spine_count)*100)
            
            
        
        else: 
            continue
        
    #save your data for each round in the analysis folder
    df_spine_data = pd.DataFrame(spine_data).to_csv(results_path + fr'/spine_data_overall_{round_folder}.csv', index=False)
    
    df_spine_type_data = pd.DataFrame(spine_type_data["filopodia"]).to_csv(results_path + fr'/spine_data_filopodia_{round_folder}.csv', index=False)
    df_spine_type_data = pd.DataFrame(spine_type_data["mushroom"]).to_csv(results_path + fr'/spine_data_mushroom_{round_folder}.csv', index=False)
    df_spine_type_data = pd.DataFrame(spine_type_data["stubby"]).to_csv(results_path + fr'/spine_data_stubby_{round_folder}.csv', index=False)
    df_spine_type_data = pd.DataFrame(spine_type_data["thin"]).to_csv(results_path + fr'/spine_data_thin_{round_folder}.csv', index=False)
    

    
    
 