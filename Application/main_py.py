# -*- coding: utf-8 -*-



from PyQt4 import QtGui, QtCore

import fonctions as f
import numpy as np
from  GpsHandle import*
from matplotlib import cm

import sys

 
from Fenetre   import *

class Fenetre(QtGui.QMainWindow,Ui_MainWindow):

   """
    classe principale :gestion des intraction IHM
    
    
    
    
    
    
   """
             

          
            
            
       
    
    
    
   def  __init__(self,parent=None):
       
     """
      Construteur 
      
      
     """
       
     QtGui.QMainWindow.__init__(self,parent)

     self.setupUi(self)
     self.timer1=QtCore.QTimer()
     self.echelle=0
     self.echelle2=0
     self.timer2=QtCore.QTimer()
     self.timer3=QtCore.QTimer()
     self.dataSource=open(path+"\\data_uv24_nmea.txt")
     self.sauvagarde=open(path+"\\sauvegarde\Data"+time.strftime("%A %d %B %Y %H:%M:%S").replace(":",".").replace("","")+".nmea","w")
     
     
     #on liste les ports disponibles 
     self.list_ports=f.listePortsDisponible()
     
     
     # on les place dans une liste
     
     if len(self.list_ports)>0:
         self.actionCOM1.setText(self.list_ports[0])
         self.actionCOM1.setEnabled(True)        
     
     #
     self.gps=GpsHandle()
     self.wayPointIti=[]
     
  
  
     #self.matplotlibwidget.figure.clear()
     #self.ax= self.matplotlibwidget.axes.imshow(image)
     self.xlim=[500,1080]
     self.ylim=[1150,800] 
     self.xlim0=[500,1080]
     self.ylim0=[1150,800] 
     self.matplotlibwidget.axes.get_yaxis().set_visible(False)
     self.matplotlibwidget.axes.get_xaxis().set_visible(False)
     self.axMap=self.matplotlibwidget.figure.add_axes([0.03,0.01, 0.99, 1])
     self.axMap.imshow(image, cmap=cm.BrBG,interpolation='gaussian')#quadric
     self.axMap.set_xlim(self.xlim)
     self.axMap.set_ylim(self.ylim)     
     self.axMap.set_xlabel("colonne ")    
     self.axMap.set_ylabel("ligne")  

#     

#mettre une limite au shema 
     self.matplotlibwidget_2.axes.get_yaxis().set_visible(False)
     self.matplotlibwidget_2.axes.get_xaxis().set_visible(False)   
     self.axConstellation=self.matplotlibwidget_2.figure.add_axes([0.14, 0.11, 0.75, 0.75], polar=True, axisbg="#00BAD5"  )
#     self.axConstellation.get_xaxis().set_visible(False)
  
     self.axConstellation.set_xticklabels([])
     self.axConstellation.scatter([],[],color=f.getColor(0), s=8,label="vitesse moyenne")  
     self.axConstellation.legend()      
     self.axConstellation.grid(True)
     self.axConstellation.set_title("Constelation", fontsize=11)#☺deplacer le titre 
      


     
     self.matplotlibwidget_3.axes.get_yaxis().set_visible(False)
     self.matplotlibwidget_3.axes.get_xaxis().set_visible(False)
     
     self.axCourbeVistesse=self.matplotlibwidget_3.figure.add_axes([0.1,0.05, 0.8, 0.85])
     self.axCourbeVistesse.set_xlabel("durée (s)")    
     self.axCourbeVistesse.set_ylabel("vitesse (m/s)")      
     self.axCourbeVistesse.plot([],[],color="#00BAD5",label="courbe de vitesse")
     self.axCourbeVistesse.plot([],[],color="#01EE2F",label="vitesse Sat")     
       
     self.axCourbeVistesse.scatter([],[],color="#E60020", s=8,label="vitesse moyenne")  
     self.axCourbeVistesse.legend()     
     self.axCourbeVistesse.grid(True)

     self.setArborescenOnlineFiles() 


     QtCore.QObject.connect(self.timer1, QtCore.SIGNAL("timeout()"), self.analyse)
     self.timer1.setInterval(200) 

     self.actionOuvrir.triggered.connect(self.setFile)
     self.actionEnregister.triggered.connect(self.enresigtrerImage)
     self.actionLancer.triggered.connect(self.start)
     self.actionArreter.triggered.connect(self.stop)
     self.actionCOM1.triggered.connect(self.setPort1)
     self.actionCOM3.triggered.connect(self.setPort6)     
     self.echelle_sliderH.valueChanged.connect(self.setEchelle)
     self.echelle_sliderV.valueChanged.connect(self.setEchelle)
     #self.matplotlibwidget.mpl_connect('pick_event',self.clickPoint)
     self.matplotlibwidget.figure.canvas.callbacks.connect('button_press_event',self.clickPoint)
   #  self.matplotlibwidget_3.mousePressEvent.connect(sel)
     
    # action.triggered.connect(self.execute)
     
     self.dessinner()
     
  
   def setPort1(self):
       """
       définit le port COM 3 comme source 
       
       
       Paramètres:
           
           aucun
       Baudrate donné par la documentation le bit de stop et le bit de parité sont donnés par la documentation    
        certains parmaètre tel que le bit de parité  se sont revélés facultatif    
       """
       self.dataSource=Serial(self.list_ports[0],4800,timeout=1)
       
       #facultatif 
       #self.dataSource.stopbits=1
       #self.dataSource.parity=None  ;
       
       
         
         
         
   def setPort4(self):
       """
       définit le port COM4 comme source 
       
       Paramètres:
           
           aucun       
       
       
       """       
       
       
       
       self.dataSource=Serial("COM4",4800,timeout=1)
        
         
   def setPort5(self):
       """
       définit le port COM6 comme source
       
       Paramètres:
           
           aucun       
       
       
       
       """       
       
       self.dataSource=Serial("COM5",4800,timeout=1)
       
         
   def setPort6(self):
       """
       définit le port COM6  comme source
       
       Paramètres:
           
           aucun       
       
       
       
       """       
       self.dataSource=Serial("COM12",4800,timeout=1)# Device name or None.,baudrate (int) – Baud rate bytesize – Number of data bits,parity – Enable parity checking. Possible values: PARITY_NONE, PARITY_EVEN, Set a read timeout value.
       self.reset()
       
                  
         
   def setFile(self): 
       
       
             """
             Permet l'ouverture d'un fichier comme source de trame NMEA
             
                    
               Paramètres:
                   
                   aucun
                   
                   
                     
             
             """
       
             fname = QtGui.QFileDialog.getOpenFileName(self, 'ouvrier un fichier ',path,"fichier (*.nmea *.txt)")
             self.dataSource=open(fname)
             self.reset()
             print(fname)
   def enresigtrerImage(self):
        """
        enregistrer une image
        
        
        """
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Enregistrer', path+'\\figures','*.png*.jpg')
        if fileName:
            print (fileName)
     
            p = QtGui.QPixmap.grabWindow(self.tabWidget.currentWidget().winId())
            p.save(fileName, fileName.split('.')[1])
            
                   
         
   def start(self):
       
       """
       Lance la lecture du port  
       """       
       self.timer1.start()       
         
   def stop(self):
       
       """
       met pause  à  la lecture du port  courant  
       """        
       
       self.timer1.stop()    
     
         
         
   def setEchelle(self):
       
       """"
       permet se déplacer sur l'image
       
       """
#       signe,signe2=1,-1
#       if      self.echelle>self.echelle_sliderH.value():
#           signe=-1
#       
#       if self.echelle2>self.echelle_sliderV.value():
#           signe2=1
#
#       print(self.echelle_sliderH.value())
       self.xlim= self.echelle_sliderH.value(),self.echelle_sliderH.value()+580 
       self.ylim=  self.echelle_sliderV.value(), self.echelle_sliderV.value()-350
  
       self.axMap.set_xlim(self.xlim)
       self.axMap.set_ylim(self.ylim)

 
       self.echelle= self.echelle_sliderH.value()                 
       self.echelle2= self.echelle_sliderV.value()   
       self.matplotlibwidget.draw()                    
         



        

   def dessinner(self):
       
             """
             dessiner la carte la constellation
             """
             self.axConstellation.cla()
             self.axConstellation.annotate("Nord", xy=((90*3.14)/180,90.1), fontsize=15) 
             self.axConstellation.annotate("Sud", xy=((270*3.14)/180,90.1), fontsize=15)              
             self.axConstellation.annotate("Ouest", xy=((180*3.14)/180,90.1), fontsize=15) 
             self.axConstellation.annotate("Est", xy=((5*3.14)/180,90.1), fontsize=15) 
            
             
             for  s in   self.gps._GpsHandle__list_satellite_v:
                 
                 elev,theta=90-float(s.getElevation()),float(s.getAzimuth())
                 self.axConstellation.scatter((theta*3.14)/180, elev,color=f.getColor(s.getSnr()), s=1000)
                 self.axConstellation.annotate("PRN"+str(s.getId()), xy=((theta*3.14)/180, elev), fontsize=15)   
             self.axConstellation.set_rmax(90)
             self.matplotlibwidget_2.draw()               
             print("   fin   -------------------------------------------##  "+str(len(self.gps._GpsHandle__list_satellite_v)))   
                



   def dessinnerSurCarte(self):
            """
            dessiner la carte et la trajectoire
            
            """
       
            print("  taille {}  ".format(self.gps._GpsHandle__i))   
            if len(self.gps._GpsHandle__i)>1:
                self.mettreInfoActtuelle()
                
            if len(self.gps._GpsHandle__i)<1:
                return 
                
            self.centrerMap(self.gps._GpsHandle__i[-1],self.gps._GpsHandle__j[-1])
            self.axMap.hold(True) 
            self.axMap.scatter(self.gps._GpsHandle__i[-2:],self.gps._GpsHandle__j[-2:],color="#010DBA", s=5)
                
            self.axMap.hold(True) 
            self.axMap.plot(self.gps._GpsHandle__i[-2:],self.gps._GpsHandle__j[-2:],color="#00BAD5",linewidth=0.6)
            self.axMap.hold(True)
            self.axMap.scatter(self.gps._GpsHandle__i[-1],self.gps._GpsHandle__j[-1],color="#FF0103", s=5)

            self.axMap.hold(True)

            self.matplotlibwidget.draw() 
            
   def dessinnerVistesse(self):
       
       
        """
        
        dessiner la courbe de vitesse
        
        """
        
        if len(self.gps._GpsHandle__list_vitesse)>2 and len(self.gps._GpsHandle__list_time)>2:
            print(self.gps._GpsHandle__list_time[-2:])
            self.axCourbeVistesse.plot(self.gps._GpsHandle__list_time[-2:],self.gps._GpsHandle__list_vitesse[-2:],color="#00BAD5")
            self.axCourbeVistesse.scatter(self.gps._GpsHandle__list_time[-1:],np.mean(self.gps._GpsHandle__list_satvitesse),color="#E60020", s=8)
            self.axCourbeVistesse.plot(self.gps._GpsHandle__list_time[-2:],self.gps._GpsHandle__list_satvitesse[-2:],color="#01EE2F")
                     
        self.matplotlibwidget_3.draw()
            
            
            
   def clickPoint(self,event):
       
       """
       detecter un point au click 
       pour le tracer de la trajectoire
       
       
       """
       
       print("Mouse ok")
       if event.inaxes is not None:
        print( event.xdata, event.ydata)
        coords=f.getglobalCordonnat(int(event.xdata),int(event.ydata),xoff,yoff,a,b,d,e)
        coords=f.get_lat_long(coords[0],coords[1])
        print(coords)
        self.wayPointIti.append(coords)

        if self.itineraireModecheckBox.isChecked():
            
            if  len(self.wayPointIti)==1 :
                self.axMap.scatter(int(event.xdata),int(event.ydata),color="#2BF350", s=50)
                self.lat_depart.setText(str(coords[1]))
                self.long_depart.setText(str(coords[0]))
                print(f.getAdresse(str(coords[1]),str(coords[0])))
                self.adresse_depart.setText(f.getAdresse(str(coords[1]),str(coords[0])))
                
                
            elif  len(self.wayPointIti)>=2 :  
                self.axMap.scatter(int(event.xdata),int(event.ydata),color="#DA1212", s=200)
                self.lat_arrivee.setText(str(coords[1]))
                self.long_arrivee.setText(str(coords[0])) 
                self.adresse_arrivee.setText(f.getAdresse(str(coords[1]),str(coords[0])))
                self.label_accueil.setText(f.getAdresse(str(coords[1]),str(coords[0])))
                traj=f.getItiniraire(self.wayPointIti[0][1],self.wayPointIti[0][0],self.wayPointIti[1][1], self.wayPointIti[1][0])
                for i in range(len(traj[0])):
                 self.axMap.scatter(traj[0][i],traj[1][i],color="#2BF350", s=20)
           
                self.axMap.plot(traj[0],traj[1],color="#00BAD5")
                self.axMap.scatter(traj[0][0],traj[1][0],color="#2BF350", s=50)  

                self.wayPointIti=[]
             
                print("trajet")
               
        else:
                self.axMap.scatter(int(event.xdata),int(event.ydata),color="#F7F501", s=7)
                self.lat_depart.setText(str(coords[1]))
                self.long_depart.setText(str(coords[0])) 
                self.adresse_depart.setText(f.getAdresse(str(coords[1]),str(coords[0])))
                print((event.x,event.y))
#                QtGui.QToolTip.showText(QtCore.QPoint(event.x,event.y),"ok",self.matplotlibwidget)
#                                
                self.wayPointIti=[]
        self.matplotlibwidget.draw()         

                          
   def analyse(self):
       """
       lancer l'analyse et mettre à jour les graphes
       """
       ligne=str(self.dataSource.readline())
       self.gps.analayseData(ligne)
       self.sauvagarde.write("{} \n".format(ligne))
       self.trames_text.append(ligne)
       self.dessinner()
       self.dessinnerSurCarte()
       self.dessinnerVistesse()
       
       
   def mettreInfoActtuelle(self):
       """
       mettre info à jour
       
       """
       self.ValeurldateActuelle.setText(self.gps._GpsHandle__date)
       self.ValeurlatitudeActuelle.setText(self.gps._GpsHandle__lat)
       self.Valeurlongitude_actuelle.setText(self.gps._GpsHandle__long)
       self.Valeurvitesse_actuelle.setText(" {} m/s".format(self.gps._GpsHandle__list_vitesse[-1]))       
       self.Valeurdistance_actuelle.setText(" {}  m".format(self.gps._GpsHandle__distance))
       self.Valeurduree.setText(" {}s".format(self.gps._GpsHandle__list_time[-1]-self.gps._GpsHandle__list_time[0]))
       self.ValeurlheureActuelle.setText(self.gps._GpsHandle__time)
       self.label_hdop_actuelle.setText(str(self.gps._GpsHandle__hdop))
       self.label_vdop_actuelle.setText(str(self.gps._GpsHandle__vdop))       


       
   def quit(self):
       
       """
       quitter le programme
       """
       self.timer1.stop()
       self.dataSource.close()
       
       self.sauvagarde.close()
       self.close()

                                             
       
       
   def main(self):
        self.show()   
        
        #self.matplotlibwidget.axes.plot(x,y)       
   def mousePressEvent(self, event):
      print("Mouse")

      

      
   def centrerMap(self,i,j):
       """
        centrer l'image une image
       """
       
       dif1=i-(self.xlim[1]+self.xlim[0])/2
       dif2=j-(self.ylim[0]+self.ylim[1])/2 
       print(" centre ({},{})  P({},{})dif2 {}".format((self.xlim[1]-self.xlim[0])/2,(self.ylim[0]-self.ylim[1])/2 ,i,j,dif2)) 
       alpha=0.1

       self.xlim= self.xlim[0]+dif1*alpha, self.xlim[1]+dif1*alpha
       self.ylim=   self.ylim[0]+alpha*dif2, self.ylim[1]+alpha*dif2
  
       self.axMap.set_xlim(self.xlim)
       self.axMap.set_ylim(self.ylim)


       self.matplotlibwidget.draw()                    
   def reset(self) :
     """
     réinitaliser tous les paramètres du programmes afin d'analyser un nouveau fichier
     """
     self.gps=GpsHandle()
     
     
     self.wayPointIti=[]
     
  
  
     #self.matplotlibwidget.figure.clear()
     #self.ax= self.matplotlibwidget.axes.imshow(image)

     self.axMap.cla()
     self.axMap.imshow(image)
     self.axMap.set_xlim(self.xlim0)
     self.axMap.set_ylim(self.ylim0)     
     self.axMap.set_xlabel("colonne ")    
     self.axMap.set_ylabel("ligne")  

     
#     

#mettre une limite au shema 
     self.axConstellation.cla()

     self.axCourbeVistesse.cla()  
     self.axCourbeVistesse.grid(True)   
     self.axCourbeVistesse.plot([],[],color="#00BAD5",label="courbe de vitesse")
     self.axCourbeVistesse.scatter([],[],color="#E60020", s=8,label="vitesse moyenne") 
     self.axCourbeVistesse.plot([],[],color="#01EE2F",label="vitesse Sat")  
     self.axCourbeVistesse.set_xlabel("durée (s)")    
     self.axCourbeVistesse.set_ylabel("vitesse (m/s)")  
     self.axCourbeVistesse.legend()      

     self.matplotlibwidget.draw()       
     self.matplotlibwidget_2.draw()  
     self.matplotlibwidget_3.draw() 
     
   def setArborescenOnlineFiles(self):
       
    pointListBox = QtGui.QTreeWidget()
    
    header=QtGui.QTreeWidgetItem(["Nom","date de création","taille(en Ko)"])
    #...
    self.treeWidget.setHeaderItem(header)   #Another alternative is setHeaderLabels(["Tree","First",...])
    
    root = QtGui.QTreeWidgetItem(self.treeWidget, ["geojoc"])
    for fi in f.getListeFichiers():
       print(fi) 
       item= QtGui.QTreeWidgetItem(root, [fi[0],fi[1]])
      # item.setIcon()

                
      
      
      
if __name__=="__main__":

    app = QtGui.QApplication(sys.argv)

    fenetre=Fenetre()
    
    app.connect(app, QtCore.SIGNAL("lastWindowClosed()"),fenetre.quit)
    
    fenetre.show()
    app.exec_()
    



        
