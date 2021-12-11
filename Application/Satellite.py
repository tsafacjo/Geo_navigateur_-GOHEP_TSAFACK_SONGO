# -*- coding: utf-8 -*-


class Satellite:
    
    def __init__(self,id,ele,az,snr):
        
    
    
        self.__id=int (id)
        self.__elevation=float(ele)
        self.__azimuth=float(az)
        self.__snr=float(snr)
        
    def __str__(self):
         
         
         return "  id  : {} , elveation : {} azimuth :{} Signal quality : {}".format( self.__id, self.__elevation,self.__azimuth,self.__snr)
        
       
    def getElevation(self):
        
     
        return self.__elevation;
        

       
    def getAzimuth(self):
        
     
        return self.__azimuth;
    def getSnr(self):
       return self.__snr
    def getId(self):
       return self.__id


