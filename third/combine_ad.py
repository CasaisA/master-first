#! /usr/bin/env python

from Configurables import DaVinci
import GaudiPython
import os
from PhysSelPython.Wrappers import DataOnDemand
from Configurables import CombineParticles, ChargedProtoParticleMaker, NoPIDsParticleMaker
from CommonParticles import StdAllNoPIDsPions, StdAllNoPIDsElectrons, StdNoPIDsUpElectrons
from CommonParticles.Utils import *

########################
## make VELO particles by hand
# first make protoparticles (needed for VELO Tracks)
myprotos = ChargedProtoParticleMaker("MyProtoParticles",
                                     Inputs = ["Rec/Track/Best"],
                                     Output = "Rec/ProtoP/MyProtoParticles")
DaVinci().UserAlgorithms +=[myprotos]

#now make the velo particles
algorithm =  NoPIDsParticleMaker ( 'StdNoPIDsVeloElectrons',
                                   DecayDescriptor = 'Electron' ,
                                   Particle = 'electron',
                                   Input = myprotos.Output)

# configure the track selector
selector = trackSelector ( algorithm,trackTypes = [ "Velo" ]  )
locations = updateDoD ( algorithm )
########################

## build all possible combinations of track types
combs = {"LL":"( ANUM( ( TRTYPE == 3 ) &  ( ABSID == 'e-' ) ) == 2 )",
         "UU":"( ANUM( ( TRTYPE == 4 ) &  ( ABSID == 'e-' ) ) == 2 )",
         "VV":"( ANUM( ( TRTYPE == 1 ) & ( ABSID == 'e-' ) ) == 2 )",
         "LU":"( ( ANUM( ( TRTYPE == 3 ) &  ( ABSID == 'e-' ) ) == 1 ) & ( ANUM( ( TRTYPE == 4 ) & ( ABSID == 'e-' ) ) == 1 ) )",
         "LV":"( ( ANUM( ( TRTYPE == 3 ) &  ( ABSID == 'e-' ) ) == 1 ) & ( ANUM( ( TRTYPE == 1 ) & ( ABSID == 'e-' ) ) == 1 ) )",
         "UV":"( ( ANUM( ( TRTYPE == 4 ) &  ( ABSID ==  'e-' ) ) == 1 ) & ( ANUM( ( TRTYPE == 1 ) & ( ABSID == 'e-' ) ) == 1 ) )"}

## build combinations
Ks2pipiee = {}
for name in combs:
    Ks2pipiee[name] = CombineParticles("TrackSel"+name+"_Ks2pipiee")
    Ks2pipiee[name].DecayDescriptor = "KS0 -> pi+ pi- e+ e-"
    Ks2pipiee[name].Preambulo=["from LoKiPhysMC.decorators import *",
                               "from LoKiPhysMC.functions import mcMatch"]
    ## only take pions mctruth matched to pions from signal...
    Ks2pipiee[name].DaughtersCuts = {"pi+"  : "mcMatch('KS0 ==>  ^pi+ pi- e+ e-' )",
                                     "pi-"  : "mcMatch('KS0 ==>  pi+ ^pi- e+ e-' )"}
    Ks2pipiee[name].CombinationCut = combs[name]
    Ks2pipiee[name].MotherCut = "ALL"
    ## input all possible daughters
    Ks2pipiee[name].Inputs =['Phys/StdAllNoPIDsPions', 'Phys/StdAllNoPIDsElectrons', 'Phys/StdNoPIDsUpElectrons', 'Phys/StdNoPIDsVeloElectrons']
    DaVinci().UserAlgorithms +=[Ks2pipiee[name]]

DaVinci().EvtMax = 0
DaVinci().DataType = "2016"
DaVinci().Simulation = True

HOME = "/eos/lhcb/wg/RD/K0S2pipiee/dsts/MC2016/Priv/Sim09cMagUpLDST/"
DaVinci().Input = map(lambda x: 'PFN:root://eoslhcb.cern.ch/'+HOME+x,os.listdir(HOME))
#DaVinci().Input 
gaudi = GaudiPython.AppMgr()
gaudi.initialize()

DEBUG = 0
TES = gaudi.evtsvc()
cbreak = 0
for i in range(1000):
    if cbreak: break
    bla = gaudi.run(1)
    for name in combs:
        ks0s = TES["Phys/TrackSel"+name+"_Ks2pipiee/Particles"]
        if not len(ks0s): continue
        print "********",name,"********"
        print "len(ks0s)",len(ks0s)
        cbreak = 1
        if DEBUG:
            myks = ks0s[0]
            print myks
            print myks.endVertex().chi2()
            print myks.pt().value()
            print myks.daughters()[0].pt().value()
            print myks.daughters()[0].proto().track().type()
            #get_mcpar(myks.daughters()[0].proto()
