# -*- coding: utf-8 -*-
import numpy as np

import fonctions as f
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import os 
import time 
im = gdal.Open('Z:\python_worksapce\geonaivateur2\ensta_2015.jpg')
nx = im.RasterXSize  #recupere les colones
ny = im.RasterYSize  #recupere les lignes
nb = im.RasterCount  #bands
xoff,a,b,yoff,d,e=im.GetGeoTransform() #recuperer les infos

   
img_valeur=[]
image =np.zeros((ny,nx,nb))
image[:,:,0]=im.GetRasterBand(1).ReadAsArray()*255
image[:,:,1]=im.GetRasterBand(2).ReadAsArray()*255
image[:,:,2]=im.GetRasterBand(3).ReadAsArray()*255
chemin=os.getcwd()+"images\\"
path=os.getcwd()