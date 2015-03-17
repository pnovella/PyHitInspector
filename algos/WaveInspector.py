
from Centella.AAlgo import AAlgo
from Centella.physical_constants import *
from Centella.system_of_units import *

from ROOT import gSystem
gSystem.Load("$GATE_DIR/lib/libGATE")

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
            
            if (pmtid < 20 ): continue # no data in those channels

            stype = pmt.GetSensorType() 
            
            gname = "Waveform_%s_%i_Trig_%i"%(stype,pmtid,self.evtid)
            
            names.append(gname)

            for tslice in data:
                
                times.append(tslice[0]*wf.GetSampWidth()/microsecond)
                
                amps.append(tslice[1])
            
            self.hman.graph(gname,times,amps)
            
            #self.hman[gname+"_graphAxis"].GetXaxis().SetRangeUser(400,401)

            pstimes,petimes,colors = [],[],[] 

            for pulse in wf.GetPulses():
            
                pstimes.append(pulse.GetStartTime())
                
                petimes.append(pulse.GetEndTime())
                
                if pulse.find_sstore("RecoPulse"): 

                    color="red"

                    pstimes[-1]=pstimes[-1]/microsecond

                    petimes[-1]=petimes[-1]/microsecond

                else: color = "blue"

                colors.append(color)
            
            #if pstimes[-1]<400: return #!!!!!

            if self.drawEach:

                self.hman.style1d()
                
                self.hman.drawGraph(gname,"APL")
                
                ymin = self.hman[gname].GetHistogram().GetYaxis().GetXmin()

                ymax = self.hman[gname].GetHistogram().GetYaxis().GetXmax()

                for stime,etime,color in zip(pstimes,petimes,colors):
                    
                    self.hman.drawLine(stime,ymin,stime,ymax,
                                       
                                       lineType=2,lineColor=color)
                    
                    self.hman.drawLine(etime,ymin,etime,ymax,

                                       lineType=2,lineColor=color)

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

        
    
