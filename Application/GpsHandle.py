# -*- coding: utf-8 -*-

from  serial import *
from Satellite import*
import  time as t 
import fonctions as f
from variables import *


mois={"01":"Janvier","02":"Fevrier " ,"03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"jullet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Decemebre"}
cardinal_name={"W":"West","N":"North","E":"East","S":"South"}

class GpsHandle :
    """
    classe utilisée pour analyser les trames gps 
    """
    def __init__(self,data=None):
        """
        constructeur 
        
        """
      
        
        self.__lat=""
        self.__long=""
        self.__alt=0

        self.__variation=0.0
        self.__vdop=0.0
        self.__hdop=0.0
        self.__waypointDes=None
        self.__lat_list=[]
        self.__long_list=[]
        self.__lat_list_conv=[]
        self.__long_list_conv=[]
        self.__vdop=0.0
        self.__hdop=0.0
        self.__count_sat_in_view=0
        self.__count_sat=0
        self.__time=''
        self.__list_time=[]
        self.__date=''
        self.__UTC_of_position=''
        self.__coordx=[]
        self.__coordy=[]
        self.__i=[]
        self.__j=[]
        self.__s=0
        self.__cart_x=0
        self.__cart_y=0
        self.__px=0
        self.__py=0
        self.__time=0

        self.__distance=0
        self.__vitesse=0
        self.__list_vitesse=[0]
        self.__list_satvitesse=[0]                      
        self.__lis=[]
        self.__list_satellite_v=[]
        self.compteGsvtrame=0
        
        
        
       
      
        
     
        
    def __str__(self):
        """
        méthode qui renvoie une descriptife de l'état de l'instance de cette classe
        """
        return " date {}  heur {}  speed {}  km/h    latitude {}   longitutude:  {}  altitude : {}  number of satellites : {}   liste des stalellites : {}  waypoint destination ".format(self.__date,self.__time,self.__speed,self.__lat,self.__long,self.__alt,self.__count_sat,self.describe__list_satellite_v(),self.__waypointDes)



    def describe__list_satellite_v(self):
        description=""
        if len(self.__list_satellite_v)!=0:
            for i in range(4):
                description+= self.__list_satellite_v[i].__str__() +"  "
        return description
        
    def request(self,query):
            self.__portCom.write(query) 
            self.__dataReceived=self.__portCom.write.read()
            
    
    def analayseData(self,data):
        """
        méthode qui analyse une trame gps 
        
        Paramètres
        ----------
        data (trame): str
            apres traitement les données extraites sont placées dans des variables d'intance
            
            
        
            
        """        

        try :    
                 data=data.replace("\\n","").replace("b","")
                # print("in 1:",data)                 
                 data=data.replace("\\r","")
                 data=data.replace("\r","")
                 data=data.replace("\n","")
                 
                 data=data.replace("'","")
                 data=data.replace(" ","")

              
                 if not data.startswith("$"):  
                     return 
                 P_data=data.split(',')                             #1

                 emetteur=P_data[0][1:3]

                 sentence=P_data[0][3:6]

                 if sentence=="GGA":
                    
                    
                    self.__count_sat= P_data[7]#                 # 7 number of satellites 
                    
                    self.__al= P_data[9]#                 # 9 Altitude
 
  
                  
                 if sentence=="RMB":
                   
                    self.__waypointDes=WayPoint(P_data[5],"{} ° {} min {}  '".format(P_data[6][0:2] ,P_data[6][2:], cardinal_name[P_data[7]]),"{} ° {} min {}  '".format(P_data[8][0:3] ,P_data[8][3:], cardinal_name[P_data[9]]))


                    
     
                    
                 if sentence=="RMC":
                     
                     
                   

                     
                    self.__time= "{}:{}:{}".format(P_data[1][0:2],P_data[1][2:4],P_data[1][4:6])#                 #1 time stamp
                    print(self.__time)
                    #  self.__=int(P_data[2]   A validity A -OK   #2            
                      
                    self.__lat="{} ° {} min {} sec {}".format(P_data[3][0:2] ,P_data[3][2:4], float(P_data[3][4:])*60, cardinal_name[P_data[4]])    #  3 laitude 
                    print("lat "+self.__lat)

                    self.__lat_list.append(self.__lat)
                    
                    self.__long="{} ° {} min {} sec {}".format(P_data[5][0:3] ,P_data[5][3:5], float(P_data[5][5:])*60, cardinal_name[P_data[6]])  #longitude          #  5

                    self.__long_list.append(self.__long)
                                   

                    try :
                      self.__list_satvitesse.append(float(P_data[7] )*0.514) #speed  
                    except:                    
                      self.__list_satvitesse.append(-1) #speed  
                       
                    
                   
                    self.__date="{} {} {}".format(P_data[9][0:2],mois[P_data[9][2:4]],"20"+P_data[9][4:6])  #Date Stamp            #9
                                                                 
    
                    self.__cart_x=round(f.get_x_y(f.conv_lat(self.__lat),f.conv_lon(self.__long))[0],0)

                    self.__cart_y=round(f.get_x_y(f.conv_lat(self.__lat),f.conv_lon(self.__long))[1],0)
                    self.__coordx.append(self.__cart_x)
                    self.__coordy.append(self.__cart_y)
                    print(self.__cart_x,self.__cart_y)
                    i=f.pt_carte(self.__cart_x,self.__cart_y,xoff,yoff,a,b,d,e)[0]
                    j=f.pt_carte(self.__cart_x,self.__cart_y,xoff,yoff,a,b,d,e)[1]


                    print(i,j)
                    times=f.convert_time(self.__time)

                    print(times)
                    self.__lis.append([self.__cart_x,self.__cart_y,times])
                    self.__i.append(i)
                    self.__j.append(j)

                    if len(self.__i)>1:
                        dist=f.distance(self.__cart_x,self.__cart_y,self.__px,self.__py)
                        print(" d vaut ",dist)
                        self.__distance+=dist
                        time=self.__lis[-1][2]-self.__lis[-2][2]


                        #self.__list_time[-1]=self.__list_time[-1]-self.__list_time[0]
                        if time!=0 :
                            self.__list_time.append(times)                             
                            
                            self.__list_vitesse.append(dist/time)
                        
                            
                            
                    self.__px,self.__py=self.__cart_x,self.__cart_y
  

       
                 if sentence=="GSA":
                    

                    self.__hdop=P_data[16]
                    self.__vdop=P_data[17].split('*')[0]
                    print("  ok   *************************"+P_data[16])
             

                    
                 if sentence=="GSV":
                    

                    self.compteGsvtrame+=1
                    if self.compteGsvtrame==4:
                      self.compteGsvtrame=1  
                      self.__list_satellite_v=[] 
                    self.__count_sat_in_view=int(P_data[3])
                    
                    
                    try :
                     self.__list_satellite_v.append(Satellite(P_data[4],P_data[5],P_data[6],P_data[7]))
                    except:
                       pass
                    try :
                        self.__list_satellite_v.append(Satellite(P_data[8],P_data[9],P_data[10],P_data[11]))
                    except:                  
                        pass
                    try :      
                        self.__list_satellite_v.append(Satellite(P_data[12],P_data[13],P_data[14],P_data[15]))
                    except:
                        pass
                    try :
                     self.__list_satellite_v.append(Satellite(P_data[16],P_data[17],P_data[18],P_data[19].split("*")[0]))#car la force du signal du denier satellite est suivi du checksum forme *.ssss
                    except:
                        pass
                        
                        
       
                    
        except Exception as er:
            print(er)
                    
                
                
                 
                 


            
             
             
             
             
             
            
            
            
            



            
            
            
        
        
        
        
        
        
        
        
        
