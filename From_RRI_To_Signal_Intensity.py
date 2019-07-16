# -*- coding: utf-8 -*-
"""
Created on Mon Oct 01 08:26:00 2018

@author: s267636
"""
import time
import lmfit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import fnmatch
#from datetime import datetime
import git
import datetime

print (str(datetime.datetime.now()))

#Test Test Test
#%%
drive='z'
book='1'
page='199'

#This sets the range of the data to be looked at for finding the peak of the Lorentzian fit.



Number_Of_Tubes=3


 #How many ramps in each run?



#dirpath ='C:\Users\s267636\Desktop\B1P'
#
dirpath= drive + ':\Data\BookBOOK\\bBOOKp'
#dirpath= 'C:\Data\BookBOOK\\bBOOKp'
dirpath=dirpath.replace('BOOK',str(book))
#dirpath= 'C:\\Data\\b1p'

#%%

def git_push():
    try:
        
        repo.git.add(update=True)
        repo.index.commit('Updated From Within Software')
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')
    finally:
        print('Code push from script succeeded')      



def GaussGetter(newlist):
    
    inputdata=np.array(newlist)
    Filtered_x=np.array(range(len(newlist)))
    mod=lmfit.models.GaussianModel()
    params=mod.guess(inputdata,x=Filtered_x)
    Gaussian_Output=mod.fit(inputdata,params, x=Filtered_x)
    outputheight=Gaussian_Output.params['height'].value
    centre=Gaussian_Output.params['center'].value
    outputheight=Gaussian_Output.params['height'].value
    Guassian_Fit=mod.fit(inputdata,params, x=Filtered_x).best_fit
    #outputheight=pd.Series(outputheight)
    
    return outputheight ##Gaussian_Output, centre, Guassian_Fit, Filtered_x);
    

def Splitter(data,Number_of_Chunks):
    
    chunklength=int(len(data)/Number_of_Chunks)
    Split_Data = zip(*[iter(data)]*chunklength)
    
    return (Split_Data)

    
    
def Split_Then_Gauss(data,Number_of_Tubes):
      
    chunklength=int(len(data)/Number_of_Tubes)
    Split_Data = zip(*[iter(data)]*chunklength)
    GaussHeights=map(GaussGetter,Split_Data)
    
    return(GaussHeights)




 

#%%
start_time= time.time()# Initial set up: Clear all the previous graphs from the screen.
plt.close('all')



rootPath = dirpath + page

pattern = '*_amplitude.csv' 

Collated_Normalised_Absorption=pd.DataFrame()
List_of_filenames = []


#my_csv=pd.read_csv('Z:\\Data\\Book1\\b1p199\\b1p199_00034\\Amp\\b1p199_00034_amplitude.csv', header=0)
for root, dirs, files in os.walk(rootPath):
    for filename in fnmatch.filter(files, pattern):
        dirlist = ( os.path.join(root, filename))
        with open(dirlist, 'r') as f:
            print (filename)
            timea=time.time()
            my_csv=pd.read_csv(f) 
            amplitudes=my_csv.drop(my_csv.columns[0], axis = 1 )
            Intensities=amplitudes

            
            heights = Intensities.apply(Split_Then_Gauss, axis=1, args=[Number_Of_Tubes])
            print ('Heights done')
            heights = heights.apply(pd.Series)
            heights.columns=['Calculated Intensity ' + str(int(col+1)) for col in heights.columns]
            consolidateddata=pd.concat([my_csv, heights],axis=1)


            consolidatedroot = root[:-4]
            consolidated_data_filename = consolidatedroot + 'consolidated_data.csv'
            consolidateddata.to_csv(consolidated_data_filename)
            timeb=time.time()
            
            print ((" %s seconds " % (timeb - timea)) +' this loop')
            print((" %s seconds " % (time.time() - start_time)) +' so far')
            print((" %s minutes " % ((time.time() - start_time)/60)) +' so far')
            
             
    
  
#%%    
repo = git.Repo(search_parent_directories=True)
sha = repo.head.object.hexsha

git_push()

readme='Date of creation: ' +str(datetime.datetime.today().strftime('%Y-%m-%d')) +'\nGit Hash of Software Used: ' +str(sha) + '\nRepositoryAddress: https://github.com/DonalbainTiresias/RRI_To_Graphs.git'  
print (readme)
textfilename=dirpath+page+'\\b'+book+'p'+page+os.path.basename(__file__)+'.txt'

with open(textfilename, "w") as text_file:
    text_file.write(readme)




