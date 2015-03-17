
from Centella.AAlgo import AAlgo
from Centella.physical_constants import *

from ROOT import gSystem
gSystem.Load("$GATE_DIR/lib/libGATE")

from ROOT import gate

class SignalsAna(AAlgo):

    def __init__(self,param=False,level = 1,label="",**kargs):

        """
        
        """
        
            
        self.name='SignalsAna'
        
        AAlgo.__init__(self,param,level,self.name,0,label,kargs)

        try: self.sType = self.strings["SENSOR_TYPE"]
        
        except KeyError: self.sType = "gate.PMT" 


    def initialize(self):

        """
        """
        
        self.m.log(1,'+++Init method of SignalsAna algorithm+++')
        
        self.bookPulHistos("S1_")

        self.bookPulHistos("S2_")
        
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
                 
                if pulse.find_sstore("RecoPulse"): 
                    
                    if self.isS1like(pulse): self.fillHistos("S1_",pulse)
                    
                    elif self.isS2like(pulse): self.fillHistos("S2_",pulse)
                
        return True

    def finalize(self):
        
        self.m.log(1,'+++End method of SignalsAna algorithm+++')

        self.drawHistos()

        return
        
    def isS1like(self,pulse):
        
        t = pulse.GetStartTime()/microsecond

        return ( t>99 and t<100 )

    def isS2like(self,pulse):
        
        t = pulse.GetStartTime()/microsecond

        return ( t>102 and t<400 )

    def drawHistos(self):
        
        self.hman.style1d()
        
        self.hman.statsPanel(1111)

        hnames = [h.split('_')[-1] for h in self.hman.keys() if "S1" not in h]
        
        for h in hnames: 

            self.hman.draw("S1_"+h,"blue")
            
            self.hman.draw("S2_"+h,"red","","same")
            
            self.wait()

    def fillHistos(self,label,pulse):
        
        
        if not pulse.GetAmplitude(): return
            
        unit = microsecond
            
        self.hman.fill(label+"Q",pulse.GetAmplitude())
        
        self.hman.fill(label+"sT",pulse.GetStartTime()/unit)
        
        self.hman.fill(label+"eT",pulse.GetEndTime()/unit)
        
        width = (pulse.GetEndTime()-pulse.GetStartTime())/unit

        self.hman.fill(label+"wT", width)

        self.hman.fill(label+"mA",pulse.GetMaxADC())
        
        return 
        

    def bookPulHistos(self,label):
        
        self.hman.h1(label+"Q","Q;Charge (ADC);Entries",1000,0,10000)
        
        self.hman.h1(label+"sT","sT;Start Time (#mus); Entries",800,0,800)

        self.hman.h1(label+"eT","eT;End Time (#mus); Entries",800,0,800)
        
        self.hman.h1(label+"wT","wT;Time Width(#mus); Entries",2000,0,200)

        self.hman.h1(label+"mA","mA;Max. Amplitude (ADC); Entries",300,0,300)

        

        return
        
