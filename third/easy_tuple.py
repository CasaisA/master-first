#! /usr/bin/env python

from Configurables import DaVinci
from Gaudi.Configuration import NTupleSvc
from Bender.MainMC import *
import GaudiPython

class MyAlg(Algo):
    def analyse(self):
        evh = TES['Rec/Header']
        tracks = TES['Rec/Track/Best']
        mytup1 = self.nTuple( self.name() )
        mytup1.column("evtNumber",evh.evtNumber())
        ntracks = 500
        for i in range(min(len(tracks),ntracks)):
            mytup1.column("track"+str(i)+"_px",tracks[i].momentum().x())
        for i in range(min(len(tracks),ntracks),ntracks):
            mytup1.column("track"+str(i)+"_px",1e6)
        mytup1.write()
        return SUCCESS

DaVinci().EvtMax = 0
DaVinci().DataType = "2012"
DaVinci().Simulation = False

HOMEEOS = 'PFN:root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb'
DaVinci().Input = [HOMEEOS+'/LHCb/Collision12/DIMUON.DST/00034958/0000/00034958_00009754_1.dimuon.dst']
DaVinci().TupleFile = "proba.root"
gaudi = GaudiPython.AppMgr()
gaudi.addAlgorithm(MyAlg("myalg"))
##

gaudi.initialize()
TES = gaudi.evtsvc()
gaudi.run(-1)
gaudi.stop()
gaudi.finalize()
