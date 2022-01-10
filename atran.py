import numpy as np
import matplotlib.pyplot as plt

from astropy.io import fits
from pathlib import Path

import re
from mechanize import Browser
from bs4 import BeautifulSoup
import urllib.request



def getAtran(dest, pwv, el, waveMin, waveMax):
  atran_url = 'https://atran.arc.nasa.gov/cgi-bin/atran/atran.cgi'
  atran_down = 'https://atran.arc.nasa.gov'

  atran_site = Browser()
  atran_site.open(atran_url)

  #Access and fill out ATRAN form constants:
  atran_site.select_form(nr=0)
  atran_site['Altitude'] = '7810'
  atran_site['Obslat'] = ['39 deg']
  atran_site['WVapor'] = str(pwv)
  atran_site['ZenithAngle'] = str(el)
  atran_site['WaveMin'] = str(waveMin)
  atran_site['WaveMax'] = str(waveMax)
  atran_site['Resolution'] = '70000'
  
  #Submit the form and get a response unless there's an error and retry (not good since it keeps retrying, but we'll have to let it slide for now): 
  try:
    response = atran_site.submit()
  except UnicodeEncodeError:
    print("Could not get response from ATRAN, retrying...")
    getAtran(dest,pwv,el,waveMin,waveMax)
    return
  
  #Get the link and append the url
  soup = response.read()
  url_append = BeautifulSoup(soup).find_all('a')[1]['href']

  #Print and Download to Destination Path:
  print(atran_down+url_append)
  urllib.request.urlretrieve(atran_down+url_append, dest)
    

#Runtime Inputs: 

minwl = input("Input Minimum Wavelength: ")
maxwl = input("Input Maximum Wavelength: ")
print('\n')

print('Inputting...')

#From Zenith angle 57 to 55 in intervals of 60 even spaces (This can be changed to the desired angles and intervals of course):
for i in np.linspace(57.0, 55.0, num=60):
    getAtran("FILEPATH/atran_" + str(minwl) + "_" + str(i) +".dat", 0, i, minwl, maxwl) 
    #print("Zenith Angle: " + str(i))
    
print("Process Completed")

#1.14-1.35, 0.96-1.11
