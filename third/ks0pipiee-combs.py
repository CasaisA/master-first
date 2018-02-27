#! /usr/bin/env python
# -*- coding: utf-8 -*-
import GaudiPython
import os
from PhysSelPython.Wrappers import DataOnDemand
from Configurables import CombineParticles, ChargedProtoParticleMaker, NoPIDsParticleMaker,DaVinci,ChargedPP2MC
from CommonParticles import StdAllNoPIDsPions, StdAllNoPIDsElectrons, StdNoPIDsUpElectrons
from CommonParticles.Utils import *
from Gaudi.Configuration import NTupleSvc,GaudiSequencer
from Bender.MainMC import *
#from ks0pipieeNtuple import *
from SomeUtils.alyabar import *   
from LinkerInstances.eventassoc import * 
#import BenderTools.TisTos
from ROOT import *
import math as m
from BenderAlgo.select import selectVertexMin

########################
## make VELO particles by hand
# first make protoparticles (needed for VELO Tracks)

## MCTRUTH MATCHING
myprotos = ChargedProtoParticleMaker("MyProtoParticles",
                                     Inputs = ["Rec/Track/Best"],
                                     Output = "Rec/ProtoP/MyProtoParticles")

protop_locations = [myprotos.Output]
charged = ChargedPP2MC("myprotos")
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
                                   AddBremPhotonTo= [],
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
    #Ks2pipiee[name].DecayDescriptor = "KS0 -> pi+ pi- e+ e-"
    if "V" in name: Ks2pipiee[name].DecayDescriptors = ["KS0 -> pi+ pi- e+ e-","KS0 -> pi+ pi- e+ e+","KS0 -> pi+ pi- e- e-"]

    else: Ks2pipiee[name].DecayDescriptor = "KS0 -> pi+ pi- e+ e-"
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
    pids = map(lambda x: abs(x.particleID().pid()),mum.endVertices()[-1].products())
    if pids.count(11)!=2: return False
    if pids.count(211)!=2: return False
    return mcpar.key()
'''
podes mirar unha cousa mais, q me entrou a dúbida? Para upstream tracksdelta charge entre mctruth e traza(e dicir, se a carga (.charge()) das trazas upstream é a correcta) Xabier, 1:13 PM e despois, cando teñas as partículas matcheadas entre electróns e upstream particles, comparar o p das particulas mctruth co p das partículas e co p das trazas. Pq pas partículas aplicamos o brem recovery e non me queda claro que pas upstream tracks sexa necesario/conveniente. A diferenza de p entre particulas e traza é q traza non ten aplicado o brem recovery(cando digo particulas a secas erfírome a particulas reco)
'''

DaVinci().EvtMax = 0
DaVinci().DataType = "2012"
DaVinci().Simulation = True
DaVinci().DDDBtag  = "dddb-20130929-1"
DaVinci().CondDBtag = "sim-20130522-1-vc-mu100"
DaVinci().Input = ["/scratch29/KsPiPiee/up/00037694_00000031_1.allstreams.dst"]
DaVinci.TupleFile = "proba.root"
gaudi = GaudiPython.AppMgr()

# combs = ['LU']
# TES = gaudi.evtsvc()
# cbreak = 0
# for i in range(10000):
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
#             if daughters[0]==daughters[1]:
#                 continue
#             else:
#                 print daughters
#                 cbreak = 1
#                 ks = ks0
#                 break



#class to produce the nTuple
c_light = 299.792458
light_cte = 1000./c_light
TES = gaudi.evtsvc()

##class to make the ntuple

class MyAlg(AlgoMC):
    def analyse(self):
        #TES = appMgr().evtsvc()
        ks0s = TES["Phys/TrackSel"+str(self.name())+"_Ks2pipiee/Particles"]
        mytup1 = self.nTuple(self.name())
        CandidateInfo = {}
        #this is for the vertex
        pvs_ = self.vselect("pvs_", ISPRIMARY)
        if not pvs_.size(): return SUCCESS
        ips2cuter = MIPCHI2(pvs_,self.geo())
        for ks in ks0s:
             ## 1:plus 2:minus
             pi1  = ks.daughters()[0]
             pi2 = ks.daughters()[1]
             e1   = ks.daughters()[2]
             e2  = ks.daughters()[3]
             daughters = map(lambda x: is_el_from_ks(x.proto()),ks.daughters())
             daughters = filter(lambda y: type(y)==int,daughters)
             if len(daughters)!=2: continue
             if daughters[0]==daughters[1]: continue
             
             
             PVips2 = VIPCHI2( ks, self.geo())
             PV = selectVertexMin(pvs_, PVips2, (PVips2 >= 0. ))
             if not PV:
                 if self.DEBUG: print "no PV there!!!!! exit"
                 self.COUNTER["weird"] +=1
                 continue
             
             
             ctau = CTAU(PV)
             KSlife_ = ctau(ks)#mm
             KSlife_ps = KSlife_*light_cte #picoseconds
             Dis2 = VDCHI2(PV)
             PVvec = vector( VX(PV), VY(PV), VZ(PV) )
             SVvec = vector( VX(ks.endVertex()), VY(ks.endVertex()), VZ(ks.endVertex()) )
             rSV = SVvec - PVvec

             KSp = vector(PX(ks), PY(ks), PZ(ks))
       
             KSpt = vtmod(KSp)
             KSips2 = PVips2(PV)
             KSip = dpr(PVvec, SVvec, KSp)



             pi1ips2, pi2ips2,e1ips2,e2ips2 = ips2cuter(pi1), ips2cuter(pi2),ips2cuter(e1),ips2cuter(e2)
             sigDOFS = Dis2(ks)

             ipscheck = min(sigDOFS, pi1ips2, pi2ips2,e1ips2, e2ips2, KSips2)
             if ipscheck < 0:
                 if self.DEBUG: print "error on IPS calculations"
                 self.COUNTER["negSq"] +=1
                ### continue, Let's decide what to do afterwards..

             sigDOFS = m.sqrt(sigDOFS)
             KSips = m.sqrt(KSips2)

             trackpi1 = pi1.proto().track()
             trackpi2 = pi2.proto().track()
             tracke1  = e1.proto().track()
             tracke2  = e2.proto().track()
             opi1, opi2,oe1,oe2 = trackpi1.position(), trackpi2.position(), tracke1.position(), tracke2.position()
             mippvs = MIP( pvs_, self.geo() )
             iptoPV = IP (PV, self.geo())
            
             e1ippvs_ = mippvs (e1) # IP
             e2ippvs_ = mippvs (e2)
             pi1ippvs_ = mippvs (pi1)
             pi2ippvs_ = mippvs (pi2)
             
             pi1ip_ = iptoPV (pi1)
             pi2ip_ = iptoPV (pi2)
             e1ip_ = iptoPV (e1)
             e2ip_ = iptoPV (e2)
             
             CandidateInfo["ipscheck"]=ipscheck
             CandidateInfo["Vchi2"]= VCHI2(ks.endVertex())

             # CandidateInfo["KSip_r"], CandidateInfo["KSips_r"] = Double(0.), Double(0.)
             # self.Geom.distance(ks, Done["refittedPV"],CandidateInfo["KSip_r"], CandidateInfo["KSips_r"])
             # CandidateInfo["KSips_r"] = float(psqrt(CandidateInfo["KSips_r"]))
             # CandidateInfo["KSip_r"] = float(CandidateInfo["KSip_r"])
             CandidateInfo["pi1ips"] = psqrt(pi1ips2)
             CandidateInfo["pi2ips"] = psqrt(pi2ips2)
             CandidateInfo["e1ips"] = psqrt(e1ips2)
             CandidateInfo["e2ips"] = psqrt(e2ips2)
             CandidateInfo["pi1mip"] = pi1ippvs_
             CandidateInfo["pi2mip"] = pi2ippvs_
             CandidateInfo["e1mip"] = e1ippvs_
             CandidateInfo["e2mip"] = e2ippvs_
             CandidateInfo["KS_ctau"] = KSlife_ ## in milimeters !!!!!
             CandidateInfo["KSlife_ps"] = KSlife_ps  ### in ps !!
             CandidateInfo["KSmass"] = M(ks)
             CandidateInfo["ks_p1"]=PX(ks)
             CandidateInfo["ks_p2"]=PY(ks)
             CandidateInfo["ks_p3"]=PZ(ks)
             CandidateInfo["ks_p"]=P(ks)
             CandidateInfo["ks_pt"]=PT(ks)
             #########################
             ##i calculate the 6 combinantions for DOCA
             ## e1pi1 e1pi2 e1e2 e2pi1 e2pi2 pi1pi2
             DOCA_func = []
             DOCA_func.append(CLAPP(e1,self.geo()))
             DOCA_func.append(CLAPP(e2,self.geo()))
             DOCA_func.append(CLAPP(pi1,self.geo()))
             DOCA = {}
             DOCA["e1pi1"]=DOCA_func[0](pi1)
             DOCA["e1pi2"]=DOCA_func[0](pi2)
             DOCA["e1e2"]=DOCA_func[0](e2)
             DOCA["e2pi1"]=DOCA_func[1](pi1)
             DOCA["e2pi2"]=DOCA_func[1](pi2)
             DOCA["pi1pi2"]=DOCA_func[2](pi2)

             DOCA_key = min(DOCA,key=DOCA.get)
             DOCA_ = DOCA[DOCA_key]
             ###################
             CandidateInfo["DOCA"]=DOCA_
             #CandidateInfo["DOCA_comb"]=DOCA_key


             CandidateInfo["e1p1"] = PX(e1)
             CandidateInfo["e1p2"] = PY(e1)
             CandidateInfo["e1p3"] = PZ(e1)
             CandidateInfo["e2p1"] = PX(e2)
             CandidateInfo["e2p2"] = PY(e2)
             CandidateInfo["e2p3"] = PZ(e2)

             CandidateInfo["pi1p1"]= PX(pi1)
             CandidateInfo["pi1p2"]= PY(pi1)
             CandidateInfo["pi1p3"]= PZ(pi1)
             CandidateInfo["pi2p1"]= PX(pi2)
             CandidateInfo["pi2p2"]= PY(pi2)
             CandidateInfo["pi2p3"]= PZ(pi2)

             CandidateInfo["e1pt"]  = PT(e1)
             CandidateInfo["e1ptot"] = P(e1)
             CandidateInfo["e2pt"]  = PT(e2)
             CandidateInfo["e2ptot"] = P(e2)

             CandidateInfo["pi1pt"]  = PT(pi1)
             CandidateInfo["pi1ptot"] = P(pi1)
             CandidateInfo["pi2pt"]  = PT(pi2)
             CandidateInfo["pi2ptot"] = P(pi2)

             CandidateInfo["e1o1"] = e1.proto().track().position().x()
             CandidateInfo["e1o2"] = e1.proto().track().position().y()
             CandidateInfo["e1o3"] = e1.proto().track().position().z()
             CandidateInfo["e2o1"] = e2.proto().track().position().x()
             CandidateInfo["e2o2"] = e2.proto().track().position().y()
             CandidateInfo["e2o3"] = e2.proto().track().position().z()

             CandidateInfo["pi1o1"] = pi1.proto().track().position().x()
             CandidateInfo["pi1o2"] = pi1.proto().track().position().y()
             CandidateInfo["pi1o3"] = pi1.proto().track().position().z()
             CandidateInfo["pi2o1"] = pi2.proto().track().position().x()
             CandidateInfo["pi2o2"] = pi2.proto().track().position().y()
             CandidateInfo["pi2o3"] = pi2.proto().track().position().z()

             CandidateInfo["SV1"] = VX(ks.endVertex())           
             CandidateInfo["SV2"] = VY(ks.endVertex())           
             CandidateInfo["SV3"] = VZ(ks.endVertex())          
             CandidateInfo["evtNum"] = TES["Rec/Header"].evtNumber()
             CandidateInfo["runNum"] = TES["Rec/Header"].runNumber()

             CandidateInfo["PV1"] = VX(PV)
             CandidateInfo["PV2"] = VY(PV)
             CandidateInfo["PV3"] = VZ(PV)
             CandidateInfo["KSips"] = KSips
             CandidateInfo["KS_IP" ] =  KSip
             CandidateInfo["KSdissig"]= sigDOFS
             #CandidateInfo["KS_pt"] = CandidateInfo["KSpt"]
             CandidateInfo["lessIPS"] = min(CandidateInfo["e1ips"], CandidateInfo["e2ips"],CandidateInfo["pi1ips"], CandidateInfo["pi2ips"] )


             CandidateInfo["e1_track_Chi2"] = TRCHI2 (e1)
             CandidateInfo["e2_track_Chi2"] = TRCHI2 (e2)

             CandidateInfo["e1_track_Chi2DoF"] = TRCHI2DOF (e1)
             CandidateInfo["e2_track_Chi2DoF"] = TRCHI2DOF (e2)

             CandidateInfo["pi1_track_Chi2"] = TRCHI2 (pi1)
             CandidateInfo["pi2_track_Chi2"] = TRCHI2 (pi2)

             CandidateInfo["pi1_track_Chi2DoF"] = TRCHI2DOF (pi1)
             CandidateInfo["pi2_track_Chi2DoF"] = TRCHI2DOF (pi2)

             theDira = DIRA(PV)
             CandidateInfo["DIRA"]=theDira(ks)
             CandidateInfo["ProbNNe1"] = PROBNNe(e1)
             CandidateInfo["ProbNNe2"]= PROBNNe(e2)
             keys = CandidateInfo.keys()
             keys.sort()
             for key in keys:
                 mytup1.column(key,CandidateInfo[key])
             mytup1.write()
        return SUCCESS


for name in combs:
    gaudi.addAlgorithm(MyAlg(name))




gaudi.initialize()
#TES = gaudi.evtsvc()
gaudi.run(2000)
gaudi.stop()
gaudi.finalize()



f = TFile('proba.root')
t = f.Get('VV/VV')
t.Show(1)
