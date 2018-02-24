#! /usr/bin/env python

import GaudiPython
import os
from PhysSelPython.Wrappers import DataOnDemand
from Configurables import CombineParticles, ChargedProtoParticleMaker, NoPIDsParticleMaker,DaVinci,ChargedPP2MC
from CommonParticles import StdAllNoPIDsPions, StdAllNoPIDsElectrons, StdNoPIDsUpElectrons
from CommonParticles.Utils import *
from Gaudi.Configuration import NTupleSvc,GaudiSequencer
from Bender.MainMC import *



########################
## make VELO particles by hand
# first make protoparticles (needed for VELO Tracks)

# myprotos = ChargedProtoParticleMaker("MyProtoParticles",
#                                      Inputs = ["Rec/Track/Best"],
#                                      Output = "Rec/ProtoP/MyProtoParticles")
# DaVinci().UserAlgorithms +=[myprotos]

## MCTRUTH MATCHING
myprotos = ChargedProtoParticleMaker("MyProtoParticles",
                                     Inputs = ["Rec/Track/Best"],
                                     Output = "Rec/ProtoP/MyProtoParticles")

protop_locations = [myprotos.Output]
charged = ChargedPP2MC('myprotos')
charged.InputData = protop_locations
myseq = GaudiSequencer("myseq")
myseq.Members +=[myprotos,charged]
DaVinci().UserAlgorithms+=[myseq]
############



## GET MCPAR FROM PROTO
def get_mcpar(proto):
    LinkRef = GaudiPython.gbl.LHCb.LinkReference()
    linker = TES["Link/Rec/ProtoP/MyProtoParticles/PP2MC"]
    ok = linker.firstReference(proto.key(), None ,LinkRef)
    if not ok: return 0
    return TES["MC/Particles"][LinkRef.objectKey()]


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
         "VV":"( ANUM( ( TRTYPE == 1 ) &  ( ABSID == 'e-' ) ) == 2 )",
         "LU":"( ( ANUM( ( TRTYPE == 3 ) &  ( ABSID == 'e-' ) ) == 1 ) & ( ANUM( ( TRTYPE == 4 ) & ( ABSID == 'e-' ) ) == 1 ) )",
         "LV":"( ( ANUM( ( TRTYPE == 3 ) &  ( ABSID == 'e-' ) ) == 1 ) & ( ANUM( ( TRTYPE == 1 ) & ( ABSID == 'e-' ) ) == 1 ) )",
         "UV":"( ( ANUM( ( TRTYPE == 4 ) &  ( ABSID == 'e-' ) ) == 1 ) & ( ANUM( ( TRTYPE == 1 ) & ( ABSID == 'e-' ) ) == 1 ) )"}

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







def is_el_from_ks(proto):
    mcpar = get_mcpar(proto)
    if not mcpar: return False
    if abs(mcpar.particleID().pid()) != 11: return False
    mum = mcpar.mother()
    if mum.particleID().pid()!=310: return False
    pids = map(lambda x: abs(x.particleID().pid()),mum.endVertices()[0].products())
    if pids.count(11)!=2: return False
    if pids.count(211)!=2: return False
    return mcpar.key()


DaVinci().EvtMax = 0
DaVinci().DataType = "2012"
DaVinci().Simulation = True
DaVinci().DDDBtag  = "dddb-20130929-1"
DaVinci().CondDBtag = "sim-20130522-1-vc-mu100"
DaVinci().Input = ["/scratch29/KsPiPiee/up/00037694_00000001_1.allstreams.dst"]
DaVinci.TupleFile = "proba.root"
gaudi = GaudiPython.AppMgr()

# DEBUG = 0
# TES = gaudi.evtsvc()
# cbreak = 0
# for i in range(1000):
#     if cbreak: break
#     bla = gaudi.run(1)
#     for name in combs:
#         if cbreak: break
#         ks0s = TES["Phys/TrackSel"+name+"_Ks2pipiee/Particles"]
#         for ks0 in ks0s:
#             daughters = map(lambda x: is_el_from_ks(x.proto()),ks0.daughters())
#             #print AMAXDOCA(ks0)
#             daughters = filter(lambda y: type(y)==int,daughters)
#             if len(daughters)!=2: continue
#             if daughters[0]==daughters[1]: continue
#             print daughters
#             cbreak = 1
#             break
#         if cbreak: break
#class to produce the nTuple    
class MyAlg(Algo):
    def analyse(self):
        ks0s = TES["Phys/TrackSel"+str(self.name())+"_Ks2pipiee/Particles"]
        mytup1 = self.nTuple(self.name())
        candidate = {}
        #this is for the vertex
        pvs_ = self.vselect("pvs_", ISPRIMARY)
        if not pvs_.size(): return SUCCESS
        ips2cuter = MIPCHI2(pvs_,self.geo())
        for ks0 in ks0s:
             piplus  = ks0.daughters()[0]
             piminus = ks0.daughters()[1]
             eplus   = ks0.daughters()[2]
             eminus  = ks0.daughters()[3]
             daughters = map(lambda x: is_el_from_ks(x.proto()),ks0.daughters())
             daughters = filter(lambda y: type(y)==int,daughters)
             if len(daughters)!=2: continue
             if daughters[0]==daughters[1]: continue
             candidate["ks0_px"]=PX(ks0)
             candidate["ks0_py"]=PY(ks0)
             candidate["ks0_pz"]=PZ(ks0)
             candidate["ks0_p"]=P(ks0)
             candidate["ks0_pt"]=PT(ks0)
             candidate["e1_px"]=PX(eplus)
             candidate["e1_py"]=PY(eplus)
             candidate["e1_pz"]=PZ(eplus)
             
             # PVips2 = VIPCHI2( ks0, self.geo())
             # PV = selectVertexMin(pvs_, PVips2, (PVips2 >= 0. ))
             # if not PV:
             #     if self.DEBUG: print "no PV there!!!!! exit"
             #     self.COUNTER["weird"] +=1
             #     continue
             #This will calculate the max DOCA of the 4 daughtes (pipiee)
              
             
             for key in candidate.keys():
                 mytup1.column(key,candidate[key])
             mytup1.write()
        return SUCCESS






combinations = ["VV"]
for name in combinations:
    gaudi.addAlgorithm(MyAlg(name))




gaudi.initialize()
TES = gaudi.evtsvc()
gaudi.run(2000)
gaudi.stop()
gaudi.finalize()




# from ROOT import *
# f = TFile('proba.root')
# t = f.Get('UV/UV')
# t.Show(1)
