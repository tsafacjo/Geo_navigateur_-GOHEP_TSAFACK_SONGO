# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 02:39:21 2017

@author: hp
"""

# -*- coding: utf-8 -*-

import numpy as np

from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import urllib3
import certifi
import json
import math
import serial as s
from variables import *
import dropbox




"""
module qui comprend des fonctions utilisées pour le projet 



"""
def distance(x1,y1,x2,y2):
    """
    calcul de la distance entre deux points
    
    Paramètres:(x1,y1)respectivemenet(x2,y2) float coordonnées cartésien du premier point et du deuxiéme point  
    
    Renvoie:
    la distance  float    
    
    
    """
    return np.sqrt((x1-x2)**2+(y1-y2)**2)
    
def convert_time(chaine):
    """
    converti  le temp au format hh:mm:ss en ssssss
    
    Paramètres:chaine (temps en hh)str
    
    
    Renvoie:
    un entier  (nombre de secondes) de type int   
        
    """
    return int(chaine[0:2])*3600+int(chaine[3:5])*60+int(chaine[6:8])
    

def getglobalCordonnat(x,y,xoff,yoff,a,b,d,e):
    """
    donne les coordonnées d'un pixel sur la carte
    
    Paramètres:
        x  numéro de la colonne int ,y numéro de la ligne int,xoff,yoff  coordonnées de l'origine de limage float,a,b,v,e,d
    
        
    Renvoie:
        (xp,yp) les coordonnes cartésiens du pixel de l'image
    
    """
    xp=a*x+b*y+xoff
    yp=d*x+e*y+yoff
    return(xp,yp)
    

   
def get_lat_long(x,y):
    
    """
    calcul la latitude et longitude d'un point connaissant ces cordonnées cartésien
    
    
    Paramètres:
        (x,y) coordonnées cartésien
    
    
    Renvoie :
        
    latitude et la longitude
    
    
    """
        
    inputRef93=2154  
    outputREPSG=4171
    point=ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(x,y)
    initSpacialRef=osr.SpatialReference()
    initSpacialRef.ImportFromEPSG(inputRef93)
    outSpacialRef=osr.SpatialReference()
    outSpacialRef.ImportFromEPSG(outputREPSG)
    coordonnateTransrom=osr.CoordinateTransformation(initSpacialRef,outSpacialRef)
    point.Transform(coordonnateTransrom)
    return point.GetX(),point.GetY()


   
def get_x_y(L,l):
    """
    calcul les coordonnées cartésiens à partir de la latitude et de la longitude
    
    Paramètres :
        L  latitude(float),longitude  l(float)
    
    
    Renvoie:
        
       x,y coordonnées cartésiens  
        
    
    """
    inputRef93_2=4326  
    outputREPSG_2=2154 


    point=ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(l,L)
    initSpacialRef=osr.SpatialReference()
    initSpacialRef.ImportFromEPSG(inputRef93_2)
    outSpacialRef=osr.SpatialReference()
    outSpacialRef.ImportFromEPSG(outputREPSG_2)
    coordonnateTransrom=osr.CoordinateTransformation(initSpacialRef,outSpacialRef)
    point.Transform(coordonnateTransrom)
    return point.GetX(),point.GetY()    

def pt_carte(x,y,xoff,yoff,a,b,d,e):
    """
    calcul la position d'un point sur l'image 
    
   
    Paramètres:
       ( x   ,y ) codronnées cartésiens ,xoff,yoff  coordonnées de l'origine de limage float,a,b,v,e,d
            
        
        
    
    
        
    Renvoie:
    
    i,j coordonnées du point sur l'image        
        
    """
    i=(e*(x-xoff)-(b*(y-yoff)))/(a*e-b*d)
    j=(a*(y-yoff)-(d)*(x-xoff))/(a*e-b*d)
    return (i,j)

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper

def conv_lat(donnees):    
    return int(donnees[5:7])/60+float(donnees[12:16])/3600+int(donnees[0:2])
def conv_lon(donnees):
    return -(int(donnees[6:8])/60+float(donnees[13:18])/3600+int(donnees[0:3]))
    







#retourne une couleur pour un signal satellite selon que le signal soit fort ou faible 

def getColor(signal):
    """
    retourne la couleur d'un satellite en fonction de la force de son signal 
    
    
    Paramètre:
        signal   : Str état du signal 
    
    
    
    Renvoie:
        code Hex :
            ' du rouge si le signal est faible ou si la valeur n'est pas bonne
            'vert signal moyen'
            'jaune signal excelent'
        
        
    """
    
    
    try:
        
     
        
        if float(signal)<25:
            
            return "#FE0114"
        elif float(signal)<43:
            return "#01EE2F"
        else:
            return "#FEFC01"

    except:
        print("ERREUR")
        return "#F7F501"

        
        
        
        
        

def getAdresse(lat,long):
    
    """
    renvoie l'adresse du point dont les coordonnées sont lat,long
    
    
    
    
    Paramètre:
        lat,long; float
    
    """


#site="https://maps.googleapis.com/maps/api/directions/json?origin=Adelaide,SA&destination=Adelaide,SA&waypoints=optimize:true|Barossa+Valley,SA|Clare,SA|Connawarra,SA|McLaren+Vale,SA&key=YOUR_API_KEY"
    lat=lat[0:7]
    long=long[0:7]
    site="https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key=AIzaSyDsYZVng2YAHW3kdhtAqEnnv_DZJRXhIqQ".format(lat,long)

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())


    r = http.request('GET',site)
    s=str(r.data).replace('b','').replace("\\n","").replace("\\","").replace(" ","").replace("'","")
    datasR = json.loads(s)
    try:
        Adress=datasR["results"][0]['formatted_address']
    except:
        return"Iconnue"
    return Adress

def getItiniraire(latD,longD,latA,longA):


    print("ok {}".format(latD))
    site="https://maps.googleapis.com/maps/api/directions/json?origin={},{}&mode={}&destination={},{}&optimizeWaypoints=true&avoid=indoor&key=AIzaSyDui1Y8hhTnWLc2-BS5tFl7HX9gclsJF94".format(latD,longD,"walking",latA,longA)
    
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    listelat,listelong=[],[]
    
    r = http.request('GET',site)
    s=str(r.data).replace('b','').replace("\\n","").replace("\\","").replace("/","").replace("'","").replace("font-size:0.9em","").replace(" ","")
    s=s[s.find("\"start_location\":")+7:s.find(",\"traf")]
    
    print(r.data)
    debut=s.find("\"lat\":")
    fin=s.find("}",debut)
    
    while debut!=-1 :
        
        donnee=s[debut+6:fin]
        print(donnee)
        print("{}- {}".format(debut,fin))
        latlong=donnee.split(",\"lng\":")
        x,y=get_x_y(float(latlong[0]),float(latlong[1]))
        
        i,j=pt_carte(x,y,xoff,yoff,a,b,d,e)
        listelat.append(i)
        listelong.append(j)
        
        debut=s.find("\"lat\":",fin)    
        fin=s.find("}",debut)

    # on supprimer les deux premiers élémnents représentant le départ et l'arrivée
#    if len(listelat)>2:
#        
#        listelat.remove(listelat[0])
#        listelat.remove(listelat[0])
#        #listelat.remove(listelat[-1])        
#        listelong.remove(listelong[0])
#        listelong.remove(listelong[0])
        #listelong.remove(listelong[-1])
# tris des données 
        print("liste avant : {}".format(listelat))         
        n = len(listelong)
        ta=listelat
        tb=listelong
        for i in range(1,n) : # on cherche k tel que ak = min(aj )ji
         k = i
         for j in range(i+1,n) :
           # distance(x1,y1,x2,y2)
           if distance(ta[k],tb[k],ta[0],tb[0]) >  distance(ta[j],tb[j],ta[0],tb[0]) :
               k = j
         ta[k],ta[i] = ta[i],ta[k] # on met par Èchange cet ÈlÈment en premiËre position
         tb[k],tb[i] = tb[i],tb[k] # on met par Èchange cet ÈlÈment en premiËre position
                                    
                                    





        
        
    print("liste {}".format(listelat))  
    return listelat,listelong 

    
def getItiniraireWithAdress(depart,arrivee):
    
    
    
    """
    
    
    
    
    Paramètres:
        
        
        depart : str adresse de départ et  arrivee: str adresse d'arrivée
    
    
    
    """



    site="https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&key=AIzaSyDui1Y8hhTnWLc2-BS5tFl7HX9gclsJF94".format(depart,arrivee)
    
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    listelat,listelong=[],[]
    
    r = http.request('GET',site)
    s=str(r.data).replace('b','').replace("\\n","").replace("\\","").replace("/","").replace("'","").replace("font-size:0.9em","").replace(" ","")
    s=s[s.find("\"start_location\":")+7:s.find(",\"traf")]
    
    print(r.data)
    debut=s.find("\"lat\":")
    fin=s.find("}",debut)
    
    while debut!=-1 :
        
        donnee=s[debut+6:fin]
        print(donnee)
        print("{}- {}".format(debut,fin))
        latlong=donnee.split(",\"lng\":")
        x,y=get_x_y(float(latlong[0]),float(latlong[1]))
        
        i,j=pt_carte(x,y,xoff,yoff,a,b,d,e)
        listelat.append(i)
        listelong.append(j)
        
        debut=s.find("\"lat\":",fin)    
        fin=s.find("}",debut)
    print(listelat)    
    return listelat,listelong             
 




def listePortsDisponible():
    """
    
    liste les ports  série disponibles
    paramètres:
    
    Renvoie:
        
    Liste_Port :list
    """
    Liste_Port=[]
    for i in range(3,20):
        try:
            p=s.Serial("COM{}".format(i),4800,timeout=1)
            if p.is_open:
                print("COM{} ok".format(i))
                Liste_Port.append("COM{}".format(i))
                p.close()
        except:        
      
            print("COM{} off".format(i))
            
    return Liste_Port
    



def getListeFichiers():
    listeFichiers=[]
    try :
        dbx = dropbox.Dropbox('y5XpGiDJvVAAAAAAAAAAJKUwS8UAZAPYfV6t1jcNcmmbEuNNAj43lKFG96ro_d4e')
    
        for entry in dbx.files_list_folder('/geonav').entries:
            f=[]
            f.append(entry.name)
            f.append(str(entry.client_modified))
            listeFichiers.append(f)
    except:
         pass
    return   listeFichiers   
    
    







      