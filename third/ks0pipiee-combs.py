#! /usr/bin/env python
# -*- coding: utf-8 -*-
import GaudiPython
import os
from PhysSelPython.Wrappers import DataOnDemand
from Configurables import CombineParticles, ChargedProtoParticleMaker, NoPIDsParticleMaker,DaVinci,ChargedPP2MC, LoKi__VertexFitter
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
from copy import copy

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
    if "V" in name:
        Ks2pipiee[name].DecayDescriptors = ["KS0 -> pi+ pi- e+ e-","KS0 -> pi+ pi- e+ e+","KS0 -> pi+ pi- e- e-"]
        Ks2pipiee[name].ParticleCombiners = {"" : "LoKi::VertexFitter"}
        Ks2pipiee[name].addTool( LoKi__VertexFitter, name="LoKi::VertexFitter" )

        
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
    if not proto: return False
    mcpar = get_mcpar(proto)
    if not mcpar: return False
    if abs(mcpar.particleID().pid()) != 11: return False
    mum = mcpar.mother()
    if not mum: return False
    if mum.particleID().pid()!=310: return False
    pids = map(lambda x: abs(x.particleID().pid()),mum.endVertices()[-1].products())
    if pids.count(11)!=2: return False
    if pids.count(211)!=2: return False
    return mcpar.key()
'''
podes mirar unha cousa mais, q me entrou a dúbida? Para upstream tracksdelta charge entre mctruth e traza(e dicir, se a carga (.charge()) das trazas upstream é a correcta) Xabier, 1:13 PM e despois, cando teñas as partículas matcheadas entre electróns e upstream particles, comparar o p das particulas mctruth co p das partículas e co p das trazas. Pq pas partículas aplicamos o brem recovery e non me queda claro que pas upstream tracks sexa necesario/conveniente. A diferenza de p entre particulas e traza é q traza non ten aplicado o brem recovery(cando digo particulas a secas erfírome a particulas reco)
'''

#tamen podo facer un modulo que faga todas as variábeis de tracking e despois mo devolva en xeito de diccionario tipo CandidateInfo
'''
def tracking(x, name):
  trackingInfo = {}
  trackingInfo["px_"+name] = px(x)
  ....
  return trackingInfo
'''
#todo o que definiu diego esta en o tes ou ben en Erasmus (Phys/BenderAlgo) ou ben en Urania (Math/SomeUtils)
DaVinci().EvtMax = 0
DaVinci().DataType = "2012"
DaVinci().Simulation = True
DaVinci().DDDBtag  = "dddb-20130929-1"
DaVinci().CondDBtag = "sim-20130522-1-vc-mu100"
DaVinci().Input = ["/scratch29/KsPiPiee/up/00037694_00000035_1.allstreams.dst"]
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
emass = 0.510998
pimass = 139.5706


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
             
             if not ks: continue
             if not ks.daughters():continue
             daughters = map(lambda x: is_el_from_ks(x.proto()),ks.daughters())
             daughters = filter(lambda y: type(y)==int,daughters)
             if len(daughters)!=2: continue
             if daughters[0]==daughters[1]: continue
             ## 1:plus 2:minus
             pi1  = ks.daughters()[0]
             pi2 = ks.daughters()[1]
             e1   = ks.daughters()[2]
             e2  = ks.daughters()[3]
             #SELECTING THE VERTEX
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
             mipchi2pvs_ = MIPCHI2(pvs_, self.geo())
             ipchi2PV = IPCHI2(PV, self.geo())
            
             e1ippvs_ = mippvs (e1) # IP
             e2ippvs_ = mippvs (e2)
             pi1ippvs_ = mippvs (pi1)
             pi2ippvs_ = mippvs (pi2)
             
             pi1ip_ = iptoPV (pi1)
             pi2ip_ = iptoPV (pi2)
             e1ip_ = iptoPV (e1)
             e2ip_ = iptoPV (e2)        #

             
             
             
             CandidateInfo["ipscheck"]=ipscheck
             CandidateInfo["SVChi2"]= VCHI2(ks.endVertex())

             
             CandidateInfo["pi1mip"] = pi1ippvs_
             CandidateInfo["pi2mip"] = pi2ippvs_
             CandidateInfo["e1mip"] = e1ippvs_
             CandidateInfo["e2mip"] = e2ippvs_
             CandidateInfo["pi1ip"]=pi1ip_
             CandidateInfo["pi2ip"]=pi2ip_
             CandidateInfo["e1ip"]=e1ip_
             CandidateInfo["e2ip"]=e2ip_
             CandidateInfo["pi1mipchi2"] = mipchi2pvs_(pi1)
             CandidateInfo["pi2mipchi2"] = mipchi2pvs_(pi2)
             CandidateInfo["e1mipchi2"] = mipchi2pvs_(e1)
             CandidateInfo["e2mipchi2"] = mipchi2pvs_(e2)

             CandidateInfo["pi1ipchi2"] = ipchi2PV(pi1)
             CandidateInfo["pi2ipchi2"] = ipchi2PV(pi2)
             CandidateInfo["e1ipchi2"] = ipchi2PV(e1)
             CandidateInfo["e2ipchi2"] = ipchi2PV(e2)
             
             CandidateInfo["Ksctau"] = KSlife_ ## in milimeters !!!!!
             CandidateInfo["KSlife_ps"] = KSlife_ps  ### in ps !!
             CandidateInfo["Ksmass"] = M(ks)
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
             if DOCA_key == "e1pi1":   CandidateInfo ["DOCA_comb"]=1
             elif DOCA_key == "e1pi2": CandidateInfo ["DOCA_comb"]=2
             elif DOCA_key == "e1e2": CandidateInfo  ["DOCA_comb"]=3
             elif DOCA_key == "e2pi1": CandidateInfo ["DOCA_comb"]=4
             elif DOCA_key == "e2pi2": CandidateInfo ["DOCA_comb"]=5
             elif DOCA_key == "pi1pi2": CandidateInfo["DOCA_comb"]=6
             else: CandidateInfo["DOCA_comb"]=7
             
        
             #KINEMATIC

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
             
             ##Invariant masses

             #for the categories LL,LU,LV,UU AND UV
             #We will consdier always a 'good' which will give us the kinematic info
             #and a 'bad' track that only will give us the kinematic constraint

             #for LU,LV the good will always be the LONG track

             #for UV it will be the upstream

             #for UU and LL it will be the one with less error in the momentum

             #######################################################################

             #Initialization of the kinematic variables
             ux = VX(ks.endVertex())-VX(PV)
             uy = VY(ks.endVertex())-VY(PV)
             uz = VZ(ks.endVertex())-VZ(PV)
             e1_mc = get_mcpar(e1.proto())
             e2_mc = get_mcpar(e2.proto())
             pi1_mc = get_mcpar(pi1.proto())
             pi2_mc = get_mcpar(pi1.proto())
             #TRUTH-V for for comparison with the fit
             ux_t = e1_mc.mother().originVertex().position().x()-e1_mc.mother().endVertices()[-1].position().x()
             uy_t = e1_mc.mother().originVertex().position().y()-e1_mc.mother().endVertices()[-1].position().y()
             uz_t = e1_mc.mother().originVertex().position().z()-e1_mc.mother().endVertices()[-1].position().z()
             
             u = TVector3(ux,uy,uz)
             u_t = TVector3(ux_t,uy_t,uz_t)
             u.SetMag(1.)
             #uprim e uprima, o vector resultante dos outros tres, que ten q ser coplanario co momento do electron/positron
             p_piplus = TVector3(PX(pi1),PY(pi1),PZ(pi1))
             p_piminus = TVector3(PX(pi2),PY(pi2),PZ(pi2))
             p_eplus = TVector3(PX(e1),PY(e1),PZ(e1))
             p_eminus = TVector3(PX(e2),PY(e2),PZ(e2))
                
        	
             uprim = p_piplus + p_piminus
             VVevent = False
             #specification of the 'good' and 'bad' electron momentums
             if (e1.proto().track().type()==1 and e2.proto().track().type()==3) or (e1.proto().track().type()==3 and e2.proto().track().type()==1) : #LV   
        	if e1.proto().track().type() == 1:
                    pgood = p_eminus
                    pbad = p_eplus
                else:
                    pgood = p_eplus
                    pbad = p_eminus

             elif (e1.proto().track().type()==4 and e2.proto().track().type()==3) or (e1.proto().track().type()==3 and e2.proto().track().type()==4) : #LU   
        	if e1.proto().track().type() == 4:
                    pgood = p_eminus
                    pbad = p_eplus
                else:
                    pgood = p_eplus
                    pbad = p_eminus
             elif (e1.proto().track().type()==4 and e2.proto().track().type()==1) or (e1.proto().track().type()==1 and e2.proto().track().type()==4) : #UV
                if e1.proto().track().type() == 1:
                    pgood = p_eminus
                    pbad = p_eplus
                else:
                    pgood = p_eplus
                    pbad = p_eminus
             elif (e1.proto().track().type()==3 and e2.proto().track().type()==3):#LL                                 
                 if e1.p().error()>=e2.p().error():
                    pgood = p_eminus
                    pbad = p_eplus
                 else:
                    pgood = p_eplus
                    pbad = p_eminus
             elif (e1.proto().track().type()==4 and e2.proto().track().type()==4):#UU
                 if e1.p().error()>=e2.p().error():
                    pgood = p_eminus
                    pbad = p_eplus
                 else:
                    pgood = p_eplus
                    pbad = p_eminus
        
             elif (e1.proto().track().type()==1 and e2.proto().track().type()==1): #LL
                VVevent = True
                #this names are simplier, actually are both equally bad :)
                pgood = p_eplus
                pbad  = p_eminus
                 
                 
             else:
                continue
             pbad_t = copy(pbad)
             pgood_t = copy(pgood)
             if not VVevent:
                
                uprim = uprim +pgood
                sinthetapbad = m.sin(u.Angle(pbad))
                sinthetauprim = m.sin(u.Angle(uprim))

                pe=sinthetauprim/sinthetapbad*uprim.Mag()
                pbad.SetMag(pe)
                
                P_piplus = TLorentzVector(); P_piplus.SetVectM(p_piplus,pimass)
                P_piminus = TLorentzVector();P_piminus.SetVectM(p_piminus,pimass)
                Pgood = TLorentzVector(); Pgood.SetVectM(pgood,emass)
                Pbad = TLorentzVector();Pbad.SetVectM(pbad,emass) 

            
                Ptot = P_piplus + P_piminus + Pgood + Pbad
            
                CandidateInfo['KSMassCo']=Ptot.M()
                ######################################### trueV
                
                sinthetapbad_t = m.sin(u_t.Angle(pbad_t))
                sinthetauprim_t = m.sin(u_t.Angle(uprim))

                pe_t=sinthetauprim_t/sinthetapbad_t*uprim.Mag()
                pbad_t.SetMag(pe_t)
                
                
                
                Pbad_t = TLorentzVector();Pbad_t.SetVectM(pbad_t,emass) 

            
                Ptot_t = P_piplus + P_piminus + Pgood + Pbad_t
            
                CandidateInfo['KSMassCoTrueV']=Ptot_t.M()
             else:
                pgood.SetMag(1.)
                pbad.SetMag(1.)
                pe = pgood + pbad
                #resultant angle of the two pions/electrons with respect to the incident ks0
                sinthetauprim = m.sin(u.Angle(uprim))
                sinthetae = m.sin(u.Angle(pe))
                pe.SetMag(uprim.Mag()*sinthetauprim/sinthetae)
                costhetapgood = m.cos(pgood.Angle(pe))
                costhetapbad = m.cos(pbad.Angle(pe))
                pgood.SetMag(pe.Mag()/(costhetapbad+costhetapgood))
                pbad.SetMag(pgood.Mag())
                
                P_piplus = TLorentzVector(); P_piplus.SetVectM(p_piplus,pimass)
                P_piminus = TLorentzVector();P_piminus.SetVectM(p_piminus,pimass)
                Pgood = TLorentzVector(); Pgood.SetVectM(pgood,emass)
                Pbad = TLorentzVector();Pbad.SetVectM(pbad,emass) 

            
                Ptot = P_piplus + P_piminus + Pgood + Pbad
            
                CandidateInfo['KSMassCo']=Ptot.M()

                ########################################### trueV

                pgood_t.SetMag(1.)
                pbad_t.SetMag(1.)
                pe_t = pgood_t + pbad_t
                #resultant angle of the two pions/electrons with respect to the incident ks0
                sinthetauprim_t = m.sin(u_t.Angle(uprim))
                sinthetae_t = m.sin(u_t.Angle(pe_t))
                pe_t.SetMag(uprim.Mag()*sinthetauprim_t/sinthetae_t)
                costhetapgood_t = m.cos(pgood_t.Angle(pe_t))
                costhetapbad_t = m.cos(pbad_t.Angle(pe_t))
                pgood_t.SetMag(pe_t.Mag()/(costhetapbad_t+costhetapgood_t))
                pbad_t.SetMag(pgood_t.Mag())
                
                
                Pgood_t = TLorentzVector(); Pgood_t.SetVectM(pgood_t,emass)
                Pbad_t = TLorentzVector();Pbad_t.SetVectM(pbad_t,emass) 

            
                Ptot_t = P_piplus + P_piminus + Pgood_t + Pbad_t
            
                CandidateInfo['KSMassCoTrueV']=Ptot.M()
                
            
        
             #TRACK TYPE
             
             CandidateInfo["e1tracktype"]=e1.proto().track().type()
             CandidateInfo["e2tracktype"]=e2.proto().track().type()
             CandidateInfo["pi1tracktype"]=pi1.proto().track().type()
             CandidateInfo["pi2tracktype"]=pi2.proto().track().type()
             

             
             #PID

             CandidateInfo["e1PIDe"]=PIDe(e1)
             CandidateInfo["e2PIDe"]=PIDe(e2)

             CandidateInfo["pi1PIDK"]=PIDK(pi1)
             CandidateInfo["pi2PIDK"]=PIDK(pi2)
             #WRONG CHARGE
             CandidateInfo["e1Charge"]=e1.charge()
             CandidateInfo["e2Charge"]=e2.charge()
             
             #MASSES FROM VECTORS (MAYBE BAD FIT)
             CandidateInfo["KSMMass"]=MM(ks)
             mothermom = e1.momentum()+e2.momentum()+pi1.momentum()+pi2.momentum()
             CandidateInfo["KSMMass-byhand"]= mothermom.M()




             #tracks and vertex

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
             CandidateInfo["evtnum"] = TES["Rec/Header"].evtNumber()
             CandidateInfo["runnum"] = TES["Rec/Header"].runNumber()

             CandidateInfo["PV1"] = VX(PV)
             CandidateInfo["PV2"] = VX(PV)
             CandidateInfo["PV3"] = VX(PV)
             CandidateInfo["PVChi2"]=VCHI2(PV)
             CandidateInfo["KSipchi2"] = KSips2
             CandidateInfo["KS_ip" ] =  KSip
             CandidateInfo["KSdissig"]= sigDOFS
             


             CandidateInfo["e1_track_Chi2"] = TRCHI2 (e1)
             CandidateInfo["e2_track_Chi2"] = TRCHI2 (e2)

             CandidateInfo["e1_track_Chi2dof"] = TRCHI2DOF (e1)
             CandidateInfo["e2_track_Chi2dof"] = TRCHI2DOF (e2)

             CandidateInfo["pi1_track_Chi2"] = TRCHI2 (pi1)
             CandidateInfo["pi2_track_Chi2"] = TRCHI2 (pi2)

             CandidateInfo["pi1_track_Chi2dof"] = TRCHI2 (pi1)
             CandidateInfo["pi2_track_Chi2dof"] = TRCHI2DOF (pi2)

             theDira = DIRA(PV)
             CandidateInfo["DIRA"]=theDira(ks)
             #PROB
             CandidateInfo["e1PROBNN"] = PROBNNe(e1)
             CandidateInfo["e2PROBNN"]= PROBNNe(e2)
             CandidateInfo["e1PROBNNghost"]=PROBNNghost(e1)
             CandidateInfo["e2PROBNNghost"]=PROBNNghost(e2)
             CandidateInfo["pi1PROBNNghost"]=PROBNNghost(pi1)
             CandidateInfo["pi2PROBNNghost"]=PROBNNghost(pi2)
             CandidateInfo["e1GP"] = TRGHOSTPROB(e1)
             CandidateInfo["e2GP"] = TRGHOSTPROB(e2)
             CandidateInfo["pi1GP"] = TRGHOSTPROB(pi1)
             CandidateInfo["pi2GP"] = TRGHOSTPROB(pi2)

             
             
             keys = CandidateInfo.keys()
             keys.sort()
             for key in keys:
                 mytup1.column(key,CandidateInfo[key])
             mytup1.write()
        return SUCCESS


for name in combs:
    gaudi.addAlgorithm(MyAlg(name))




gaudi.initialize()
gaudi.run(-1)
gaudi.stop()
gaudi.finalize()

