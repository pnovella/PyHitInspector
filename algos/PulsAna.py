
from Centella.AAlgo import AAlgo
from Centella.physical_constants import *

from ROOT import gSystem
gSystem.Load("$GATE_DIR/lib/libGATE")

from ROOT import gate

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
        
        self.bookPulHistos("RP_")

        self.bookPulHistos("ART_")
        
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
                    
                    self.fillHistos("RP_",pulse)
                    
                else: self.fillHistos("ART_",pulse)
                
        return True

    def finalize(self):
        
        self.m.log(1,'+++End method of PulsAna algorithm+++')

        self.drawHistos()

        return

    def drawHistos(self):
        
        self.hman.style1d()
        
        self.hman.statsPanel(1111)

        hnames = [h.split('_')[-1] for h in self.hman.keys() if "ART" not in h]
        
        for h in hnames: 

            self.hman.draw("ART_"+h,"blue")
            
            self.hman.draw("RP_"+h,"red","","same")
            
            self.wait()

    def fillHistos(self,label,pulse):
        
        if label=="RP_": 
            
            if not pulse.GetAmplitude(): return
            
            unit = microsecond
            
        else: unit = 1.

        self.hman.fill(label+"Q",pulse.GetAmplitude())
        
        self.hman.fill(label+"sT",pulse.GetStartTime()/unit)
        
        self.hman.fill(label+"eT",pulse.GetEndTime()/unit)
        
        width = (pulse.GetEndTime()-pulse.GetStartTime())/unit

        self.hman.fill(label+"wT", width)

        self.hman.fill(label+"mA",pulse.GetMaxADC())
        
        self.hman.fill(label+"QT",pulse.GetAmplitude(),
                       
                       pulse.GetStartTime()/unit)

        self.hman.fill(label+"WT",width,pulse.GetStartTime()/unit)

        self.hman.fill(label+"AT",pulse.GetMaxADC(),pulse.GetStartTime()/unit)

        return 
        

    def bookPulHistos(self,label):
        
        self.hman.h1(label+"Q","Q;Charge (ADC);Entries",1000,0,1000)
        
        self.hman.h1(label+"sT","sT;Start Time (#mus); Entries",800,0,800)

        self.hman.h1(label+"eT","eT;End Time (#mus); Entries",800,0,800)
        
        self.hman.h1(label+"wT","wT;Time Width(#mus); Entries",2000,0,100)

        self.hman.h1(label+"mA","mA;Max. Amplitude (ADC); Entries",100,0,100)

        self.hman.h2(label+"QT","QT;Charge (ADC); Start Time (#mus);",
                     
                     1000,0,1000,200,0,400)


        self.hman.h2(label+"WT","WT;Width (#mus); Start Time (#mus);",
                     
                     100,0,100,200,0,400)
        
        self.hman.h2(label+"AT","AT;Max. amplitude (ADC); Start Time (#mus);",
                     
                     100,0,100,200,0,400)

        return
        
