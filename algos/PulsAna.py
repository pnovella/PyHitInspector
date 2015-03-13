
from Centella.AAlgo import AAlgo
from Centella.physical_constants import *

class PulsAna(AAlgo):

    def __init__(self,param=False,level = 1,label="",**kargs):

        """
        
        """
        
            
        self.name='PulsAna'
        
        AAlgo.__init__(self,param,level,self.name,0,label,kargs)

        try: self.sType = self.strings["SENSOR_TYPE"]
        
        except KeyError: self.sType = "gate.PMT" 


    def initialize(self):

        """
        """
        
        self.m.log(1,'+++Init method of PulsAna algorithm+++')
        
        return

    def execute(self,event=""):

        """
        """

        self.evtid = event.GetEventID()

        if self.sType: pmts = event.GetHits(eval(self.sType))
        
        else: pmts = event.GetHits()
          
        for pmt in pmts: 

            wf = pmt.GetWaveform()

            pmtid = pmt.GetSensorID() 
            
            if (pmtid < 20 ): continue # no data in those channels

             for pulse in wf.GetPulses():
                 
                if pulse.find_sstore("RecoPulse"): self.fillHistos("RP")
                
                else: self.fillHistos("ART")

        return True

    def finalize(self):

        
        self.m.log(1,'+++End method of PulsAna algorithm+++')

        return

    
    def bookHistosHistos(self,label):
        
        self.hman.h1(label+"Q","Q;Charge (ADC);Entries",100,0,1000)
        
        self.hman.h1(label+"sT","sT;Start Time (#mus); Entries",100,0,800)

        self.hman.h1(label+"eT","eT;End Time (#mus); Entries",100,0,800)

        return
        
