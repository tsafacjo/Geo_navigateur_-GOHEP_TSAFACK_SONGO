# -*- coding: utf-8 -*-

class WayPoint :
    def __init__(self,id="",lat="",long="",alt=0):
        
        
        self.__id=id
        self.__lat=lat 
        self.__long=long
        self.__alt=alt 
        
    def __str__(self):

        return " id {} latitude  {} longitude {} alt {}".format(self.__id,self.__lat,self.__long,self.__alt) 
        
        
        
        
        