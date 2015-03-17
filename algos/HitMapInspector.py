
from Centella.AAlgo import AAlgo
from Centella.physical_constants import *

from ROOT import gSystem
gSystem.Load("$GATE_DIR/lib/libGATE")

from ROOT import gate

from math import sqrt

class HitMapInspector(AAlgo):

    def __init__(self,param=False,level = 1,label="",**kargs):

        """
        """
        
        self.name='WaveInspector'
        
        AAlgo.__init__(self,param,level,self.name,0,label,kargs)
        
        try: self.sType = self.strings["SENSOR_TYPE"]
        
        except KeyError: self.sType = "" 
        
       
        #try: self.drawEach = self.ints["DRAW_EACH"]
        
        #except KeyError: self.drawEach = False 

    def initialize(self):

        """        
        """
        
        self.m.log(1,'+++Init method of WaveInspector algorithm+++')
        

        return

    def execute(self,event=""):

        """            
        """
        
        self.evtid = event.GetEventID()

        if self.sType: maps = event.GetHitMaps(eval(self.sType))
        
        else: maps = event.GetHitMaps()
        
        for tmap in maps: 
            
            print "Map of Signal", tmap.GetSignalType()
            print "--------------------------"
            
            for i in range(len(tmap.GetTimeMap())):
                
                for ch, amp in zip(tmap.GetChannels(i),tmap.GetAmplitudes(i)):

                    print ch, amp

        return True

           
    def finalize(self):

        self.m.log(1,'+++End method of WaveInspector algorithm+++')

        return
    
   
    
