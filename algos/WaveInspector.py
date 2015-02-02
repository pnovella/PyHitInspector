
from Centella.AAlgo import AAlgo
from Centella.physical_constants import *

from ROOT import gSystem
gSystem.Load("$GATE_LIB/libGATE")

from ROOT import gate

from math import sqrt

class WaveInspector(AAlgo):

    def __init__(self,param=False,level = 1,label="",**kargs):

        """
        """
        
        self.name='WaveInspector'
        
        AAlgo.__init__(self,param,level,self.name,0,label,kargs)
        
        try: self.sType = self.strings["SENSOR_TYPE"]
        
        except KeyError: self.sType = "" 

        try: self.drawEach = self.ints["DRAW_EACH"]
        
        except KeyError: self.drawEach = False 

    def initialize(self):

        """        
        """
        
        self.m.log(1,'+++Init method of WaveInspector algorithm+++')
        

        return

    def execute(self,event=""):

        """            
        """
        
        self.evtid = event.GetEventID()

        if self.sType: pmts = event.GetHits(eval(self.sType))
        
        else: pmts = event.GetHits()
        
        self.npmts = len(pmts)
      
        names = []

        for pmt in pmts: 
            
            times, amps = [],[]
            
            wf = pmt.GetWaveform()
            
            data = wf.GetData()
            
            pmtid = pmt.GetSensorID() 
            
            stype = pmt.GetSensorType() 
            
            gname = "Waveform_%s_%i_Trig_%i"%(stype,pmtid,self.evtid)
            
            names.append(gname)

            for tslice in data:

                times.append(tslice[0])
                
                amps.append(tslice[1])
            
            self.hman.graph(gname,times,amps)

            pstimes,petimes = [],[] 

            for pulse in wf.GetPulses():
                
                pstimes.append(pulse.GetStartTime())
                
                petimes.append(pulse.GetEndTime())
                
            if self.drawEach:

                self.hman.style1d()
                
                self.hman.drawGraph(gname,"APL")
                
                ymin = self.hman[gname].GetHistogram().GetYaxis().GetXmin()

                ymax = self.hman[gname].GetHistogram().GetYaxis().GetXmax()

                for stime,etime in zip(pstimes,petimes):
                    
                    self.hman.drawLine(stime,ymin,stime,ymax,
                                       
                                       lineType=2,lineColor="red")

                    self.hman.drawLine(etime,ymin,etime,ymax,

                                       lineType=2,lineColor="red")

                self.wait()

        self.drawWaveforms(names);

        return True
        
    def finalize(self):

        self.m.log(1,'+++End method of WaveInspector algorithm+++')

        return
    
    def drawWaveforms(self,names):
        
        zones = int(sqrt(self.npmts))
        
        self.hman.zones(zones,zones+1)
        
        for name in names:
           
            self.hman.style1d()
            
            self.hman.drawGraph(name,"AP")
            
        self.wait()

        return

        
    
