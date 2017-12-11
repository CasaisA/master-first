#! /usr/bin/env python

## CONFIGURE DAVINCI (GENERAL CONFIGURATION OF THE JOB)
from Configurables import DaVinci, ChargedPP2MC, ChargedProtoParticleMaker
import GaudiPython
from Gaudi.Configuration import *
import pandas as pd
import math as m
import pickle
import os
from ROOT import *
import numpy as np
import sys

DaVinci().EvtMax = 0
DaVinci().DataType = "2012"
DaVinci().Simulation = True
## These are for data tags (magnet up or down?)
DaVinci().DDDBtag  = "dddb-20130929-1"
DaVinci().CondDBtag = "sim-20130522-1-vc-mu100"
#sys.argv = [0,1,1000]
## INPUT DSTS, POTENTIALLY ADD MORE
magnet='up'
dst_file = []
for i in xrange(4,71):
        i = str(i)
        if int(i)<10:
                dst_file_name = '/scratch29/KsPiPiee/'+magnet+'00037694_0000000'+i+'_1.allstreams.dst'
        else:
                dst_file_name = '/scratch29/KsPiPiee/'+magnet+'/00037694_000000'+i+'_1.allstreams.dst'

        if os.path.isfile(dst_file_name):
                dst_file.append(dst_file_name)

DaVinci().Input = dst_file

f1 = TFile('/scratch13/acasais/second/KsPiPiee-root/KsPiPiee-VELO-long'+str(sys.argv[1])+'-'+str(sys.argv[2])+'.root','recreate')
t1 = TTree('mctruth','mctruth')
t2 = TTree('reco','reco')
t3 = TTree('kS0_truth','kS0_truth')
truthd = {}
recod = {}
ks0d = {}
truthd_px=np.zeros(1,dtype=float)
truthd_py=np.zeros(1,dtype=float)
truthd_pz=np.zeros(1,dtype=float)
truthd_pT=np.zeros(1,dtype=float)
truthd_p=np.zeros(1,dtype=float)
truthd_eta=np.zeros(1,dtype=float)
truthd_phi=np.zeros(1,dtype=float)
truthd_pid=np.zeros(1,dtype=float)
truthd_evtid = np.zeros(1,dtype=float)

t1.Branch('evt_id',truthd_evtid,'evt_id/D')
t1.Branch('px',truthd_px,'px/D')
t1.Branch('py',truthd_py,'py/D')
t1.Branch('pz',truthd_pz,'pz/D')
t1.Branch('p',truthd_p,'p/D')
t1.Branch('pT',truthd_pT,'pT/D')
t1.Branch('eta',truthd_eta,'eta/D')
t1.Branch('phi',truthd_phi,'phi/D')
t1.Branch('pid',truthd_pid,'pid/D')

recod['evt_id']=np.zeros(1,dtype=float)
recod['px']=np.zeros(1,dtype=float)
recod['py']=np.zeros(1,dtype=float)
recod['pz']=np.zeros(1,dtype=float)
recod['pT']=np.zeros(1,dtype=float)
recod['p']=np.zeros(1,dtype=float)
recod['px_truth']=np.zeros(1,dtype=float)
recod['py_truth']=np.zeros(1,dtype=float)
recod['pz_truth']=np.zeros(1,dtype=float)
recod['pT_truth']=np.zeros(1,dtype=float)
recod['p_truth']=np.zeros(1,dtype=float)
recod['eta']=np.zeros(1,dtype=float)
recod['phi']=np.zeros(1,dtype=float)
recod['eta_truth']=np.zeros(1,dtype=float)
recod['phi_truth']=np.zeros(1,dtype=float)
recod['pid']=np.zeros(1,dtype=float)
recod['trck_type']=np.zeros(1,dtype=float)
recod['mother_key']=np.zeros(1,dtype=float)
recod['mother_px']=np.zeros(1,dtype=float)
recod['mother_py']=np.zeros(1,dtype=float)
recod['mother_pz']=np.zeros(1,dtype=float)
recod['mother_p']=np.zeros(1,dtype=float)
recod['mother_pT']=np.zeros(1,dtype=float)
recod['mother_eta']=np.zeros(1,dtype=float)
recod['mother_phi']=np.zeros(1,dtype=float)

t2.Branch('evt_id',recod['evt_id'],'evt_id/D')
t2.Branch('px',recod['px'],'px/D')
t2.Branch('py',recod['py'],'py/D')
t2.Branch('pz',recod['pz'],'pz/D')
t2.Branch('p',recod['p'],'p/D')
t2.Branch('pT',recod['pT'],'pT/D')
t2.Branch('eta',recod['eta'],'eta/D')
t2.Branch('phi',recod['phi'],'phi/D')
t2.Branch('pid',recod['pid'],'pid/D')
t2.Branch('px_truth',recod['px_truth'],'px_truth/D')
t2.Branch('py_truth',recod['py_truth'],'py_truth/D')
t2.Branch('pz_truth',recod['pz_truth'],'pz_truth/D')
t2.Branch('p_truth',recod['p_truth'],'p_truth/D')
t2.Branch('pT_truth',recod['pT_truth'],'pT_truth/D')
t2.Branch('eta_truth',recod['eta_truth'],'eta_truth/D')
t2.Branch('phi_truth',recod['phi_truth'],'phi_truth/D')
t2.Branch('mother_key',recod['mother_key'],'mother_key/D')
t2.Branch('trck_type',recod['trck_type'],'trck_type/D')
t2.Branch('mother_px',recod['mother_px'],'mother_px/D')
t2.Branch('mother_py',recod['mother_py'],'mother_py/D')
t2.Branch('mother_pz',recod['mother_pz'],'mother_pz/D')
t2.Branch('mother_pT',recod['mother_pT'],'mother_pT/D')
t2.Branch('mother_p',recod['mother_p'],'mother_p/D')
t2.Branch('mother_phi',recod['mother_phi'],'mother_phi/D')
t2.Branch('mother_eta',recod['mother_eta'],'mother_eta/D')

ks0d['evt_id']=np.zeros(1,dtype=float)
ks0d['run_id']=np.zeros(1,dtype=float)
ks0d['px']=np.zeros(1,dtype=float)
ks0d['py']=np.zeros(1,dtype=float)
ks0d['pz']=np.zeros(1,dtype=float)
ks0d['pT']=np.zeros(1,dtype=float)
ks0d['p']=np.zeros(1,dtype=float)
ks0d['eta']=np.zeros(1,dtype=float)
ks0d['phi']=np.zeros(1,dtype=float)
ks0d['pid']=np.zeros(1,dtype=float)
ks0d['PV_x']=np.zeros(1,dtype=float)
ks0d['PV_y']=np.zeros(1,dtype=float)
ks0d['PV_z']=np.zeros(1,dtype=float)
ks0d['SV_x']=np.zeros(1,dtype=float)
ks0d['SV_y']=np.zeros(1,dtype=float)
ks0d['SV_z']=np.zeros(1,dtype=float)
ks0['eminus_px']=np.zeros(1,dtype=float)
ks0['eminus_py']=np.zeros(1,dtype=float)
ks0['eminus_pz']=np.zeros(1,dtype=float)
ks0['eminus_pT']=np.zeros(1,dtype=float)
ks0['eminus_p']=np.zeros(1,dtype=float)
ks0['eminus_eta']=np.zeros(1,dtype=float)
ks0['eminus_phi']=np.zeros(1,dtype=float)
ks0['piminus_px']=np.zeros(1,dtype=float)
ks0['piminus_py']=np.zeros(1,dtype=float)
ks0['piminus_pz']=np.zeros(1,dtype=float)
ks0['piminus_pT']=np.zeros(1,dtype=float)
ks0['piminus_p']=np.zeros(1,dtype=float)
ks0['piminus_eta']=np.zeros(1,dtype=float)
ks0['piminus_phi']=np.zeros(1,dtype=float)

ks0['eplus_px']=np.zeros(1,dtype=float)
ks0['eplus_py']=np.zeros(1,dtype=float)
ks0['eplus_pz']=np.zeros(1,dtype=float)
ks0['eplus_pT']=np.zeros(1,dtype=float)
ks0['eplus_p']=np.zeros(1,dtype=float)
ks0['eplus_eta']=np.zeros(1,dtype=float)
ks0['eplus_phi']=np.zeros(1,dtype=float)
ks0['piplus_px']=np.zeros(1,dtype=float)
ks0['piplus_py']=np.zeros(1,dtype=float)
ks0['piplus_pz']=np.zeros(1,dtype=float)
ks0['piplus_pT']=np.zeros(1,dtype=float)
ks0['piplus_p']=np.zeros(1,dtype=float)
ks0['piplus_eta']=np.zeros(1,dtype=float)
ks0['piplus_phi']=np.zeros(1,dtype=float)

t3.Branch('evt_id',ks0d['evt_id'],'evt_id/D')
t3.Branch('run_id',ks0d['run_id'],'run_id/D')
t3.Branch('px',ks0d['px'],'px/D')
t3.Branch('py',ks0d['py'],'py/D')
t3.Branch('pz',ks0d['pz'],'pz/D')
t3.Branch('p',ks0d['p'],'p/D')
t3.Branch('pT',ks0d['pT'],'pT/D')
t3.Branch('eta',ks0d['eta'],'eta/D')
t3.Branch('phi',ks0d['phi'],'phi/D')
t3.Branch('pid',ks0d['pid'],'pid/D')
t3.Branch('PV_x',ks0d['PV_x'],'PV_x/D')
t3.Branch('PV_y',ks0d['PV_y'],'PV_y/D')
t3.Branch('PV_z',ks0d['PV_z'],'PV_z/D')
t3.Branch('SV_x',ks0d['SV_x'],'SV_x/D')
t3.Branch('SV_y',ks0d['SV_y'],'SV_y/D')
t3.Branch('SV_z',ks0d['SV_z'],'SV_z/D')

t3.Branch('eminus_px',ks0d['eminus_px'],'eminus_px/D')
t3.Branch('eminus_py',ks0d['eminus_py'],'eminus_py/D')
t3.Branch('eminus_pz',ks0d['eminus_pz'],'eminus_pz/D')
t3.Branch('eminus_pT',ks0d['eminus_pT'],'eminus_pT/D')
t3.Branch('eminus_p',ks0d['eminus_p'],'eminus_p/D')
t3.Branch('eminus_eta',ks0d['eminus_eta'],'eminus_eta/D')
t3.Branch('eminus_phi',ks0d['eminus_phi'],'eminus_phi/D')

t3.Branch('piminus_px',ks0d['piminus_px'],'piminus_px/D')
t3.Branch('piminus_py',ks0d['piminus_py'],'piminus_py/D')
t3.Branch('piminus_pz',ks0d['piminus_pz'],'piminus_pz/D')
t3.Branch('piminus_pT',ks0d['piminus_pT'],'piminus_pT/D')
t3.Branch('piminus_p',ks0d['piminus_p'],'piminus_p/D')
t3.Branch('piminus_eta',ks0d['piminus_eta'],'piminus_eta/D')
t3.Branch('piminus_phi',ks0d['piminus_phi'],'piminus_phi/D')

t3.Branch('eplus_px',ks0d['eplus_px'],'eplus_px/D')
t3.Branch('eplus_py',ks0d['eplus_py'],'eplus_py/D')
t3.Branch('eplus_pz',ks0d['eplus_pz'],'eplus_pz/D')
t3.Branch('eplus_pT',ks0d['eplus_pT'],'eplus_pT/D')
t3.Branch('eplus_p',ks0d['eplus_p'],'eplus_p/D')
t3.Branch('eplus_eta',ks0d['eplus_eta'],'eplus_eta/D')
t3.Branch('eplus_phi',ks0d['eplus_phi'],'eplus_phi/D')

t3.Branch('piplus_px',ks0d['piplus_px'],'piplus_px/D')
t3.Branch('piplus_py',ks0d['piplus_py'],'piplus_py/D')
t3.Branch('piplus_pz',ks0d['piplus_pz'],'piplus_pz/D')
t3.Branch('piplus_pT',ks0d['piplus_pT'],'piplus_pT/D')
t3.Branch('piplus_p',ks0d['piplus_p'],'piplus_p/D')
t3.Branch('piplus_eta',ks0d['piplus_eta'],'piplus_eta/D')
t3.Branch('piplus_phi',ks0d['piplus_phi'],'piplus_phi/D')







## MCTRUTH MATCHING
myprotos = ChargedProtoParticleMaker("MyProtoParticles",
                                     Inputs = ["Rec/Track/Best"],
                                     Output = "Rec/ProtoP/MyProtoParticles")

protop_locations = [myprotos.Output]

ChargedPP2MC().InputData = protop_locations
myseq = GaudiSequencer("myseq")
myseq.Members +=[myprotos,ChargedPP2MC()]
DaVinci().UserAlgorithms+=[myseq]
############

gaudi = GaudiPython.AppMgr()

gaudi.initialize()
TES = gaudi.evtsvc()
#t1.SetAutoSave(-200)
#t2.SetAutoSave(-200)
#t3.SetAutoSave(-200)
## GET MCPAR FROM PROTO
def get_mcpar(proto):
    LinkRef = GaudiPython.gbl.LHCb.LinkReference()
    linker = TES["Link/Rec/ProtoP/MyProtoParticles/PP2MC"]
    ok = linker.firstReference(proto.key(), None ,LinkRef)
    if not ok: return 0
    return TES["MC/Particles"][LinkRef.objectKey()]

cks0=0
ctruth=0
creco= 0
counter = 0
#RANGE IS AS BIG AS YOU WANT IT TO BE
if int(sys.argv[1])>1: 
	gaudi.run(int(sys.argv[1])-1)
for i in range(int(sys.argv[2])-int(sys.argv[1])+1):
    counter+=1
    c1 = gaudi.run(1)
    tracks = TES["Rec/Track/Best"]
    mcparticles = TES["MC/Particles"]
    myprotos = TES["Rec/ProtoP/MyProtoParticles"]
    
    
    mother_key = 0
    for particle in mcparticles:
	    #tipicas sentencias para evitar que unha particula corrupta entre no bucle
	    if not particle: continue
	    if not particle.momentum: continue
            products = map(lambda x: x,particle.endVertices()[-1].products())
	    products = filter(lambda x: abs(x.particleID().pid())==11 or abs(x.particleID().pid())==211,products)
	    products_pid = map(lambda x: x.particleID().pid(),products)
	    if particle.particleID().pid()==310 and (11 in products_pid) and (-11 in products_pid) and (211 in products_pid) and (-211 in products_pid):
		    
	    	    ks0d['evt_id'][0]= TES['Rec/Header'].evtNumber()
		    ks0d['run_id'][0]= TES['Rec/Header'].runNumber()
	    	    ks0d['px'][0]=particle.momentum().x()
	    	    ks0d['py'][0]=particle.momentum().y()
	    	    ks0d['pz'][0]=particle.momentum().z()
	    	    ks0d['p'][0]=particle.p()
	    	    ks0d['pT'][0]=particle.pt()
	    	    ks0d['eta'][0]=particle.momentum().eta()
	    	    ks0d['phi'][0]=particle.momentum().phi()
	    	    ks0d['pid'][0]=particle.particleID().pid()
	    	    ks0d['PV_x'][0]=particle.originVertex().position().x()
	    	    ks0d['PV_y'][0]=particle.originVertex().position().y()
	    	    ks0d['PV_z'][0]=particle.originVertex().position().z()
	    	    ks0d['SV_x'][0]=particle.endVertices()[-1].position().x()
	    	    ks0d['SV_y'][0]=particle.endVertices()[-1].position().y()
	    	    ks0d['SV_z'][0]=particle.endVertices()[-1].position().z()
		    t3.Fill()
		    fill_ks0 = False
		    cks0+=1
		    if not cks0%100:
			    t3.AutoSave()
		    
	    
			    
	    
	    
	    if (211 in products) and (-211 in products) and (11 in products) and (-11 in products) and flag_mother:
		    truthd_px[0]=particle.momentum().x()
		    truthd_py[0]=particle.momentum().y()
		    truthd_pz[0]=particle.momentum().z()
		    truthd_pT[0]=particle.pt()
		    truthd_p[0]=particle.p()
		    truthd_eta[0]=particle.momentum().eta()
		    truthd_phi[0]=particle.momentum().phi()
		    truthd_pid[0]=particle.particleID().pid()
		    truthd_evtid[0] = TES['Rec/Header'].evtNumber()
		    t1.Fill()
		    ctruth+=1
		    if not ctruth%100:
			    
			    t1.AutoSave()

		    fill_ks0=False
		    if mother_key != mother.key():
			    mother_key = mother.key()
			    fill_ks0 = True
	    
	    
	   
		    
		   
    for proto in myprotos:
	    
	    track = proto.track()
	    mcpar = get_mcpar(proto)
	    if mcpar == 0: continue
	    mother = mcpar.mother()
	    
	    if not mother: continue 
	    if not len(mother.endVertices()) or not mother.momentum() or not mother: continue
	    products =map(lambda x: x.particleID().pid(),mother.endVertices()[-1].products())
	    
	    
	    
	    #print end_vertices
	    if 211 in products and -211 in products and 11 in\
	       products and -11 in products:
		    recod['px'][0]=track.momentum().x()
		    recod['py'][0]=track.momentum().y()
		    recod['pz'][0]=track.momentum().z()
		    recod['pT'][0]=track.pt()
		    recod['p'][0]=track.p()
		    recod['px_truth'][0]=mcpar.momentum().x()
		    recod['py_truth'][0]=mcpar.momentum().y()
		    recod['pz_truth'][0]=mcpar.momentum().z()
		    recod['pT_truth'][0]=mcpar.pt()
		    recod['p_truth'][0]=mcpar.p()
		    recod['eta'][0]=track.momentum().eta()
		    recod['phi'][0]=track.momentum().phi()
		    recod['eta_truth'][0]=mcpar.momentum().eta()
		    recod['phi_truth'][0]=mcpar.momentum().phi()
		    recod['pid'][0]=mcpar.particleID().pid()
		    recod['trck_type'][0]=track.type()
		    recod['mother_key'][0]=float(str(TES['Rec/Header'].runNumber())+str(TES['Rec/Header'].evtNumber())+str(mcpar.mother().key()))
		    recod['mother_px'][0]=mother.momentum().x()
		    recod['mother_py'][0]=mother.momentum().y()
		    recod['mother_pz'][0]=mother.momentum().z()
		    recod['mother_p'][0]=mother.p()
		    recod['mother_pT'][0]=mother.pt()
		    recod['mother_eta'][0]=mother.momentum().eta()
		    recod['mother_phi'][0]=mother.momentum().phi()
		    recod['evt_id'][0]=TES['Rec/Header'].evtNumber()
		    t2.Fill()
		    creco+=1
		    if not creco%100:
			    t2.AutoSave()
f1.cd()	
f1.Write()
f1.Close()	
# with open('/scratch13/acasais/second/task1/truth-500runs.p', 'wb') as f:
#     pickle.dump(mctruth, f)

# with open('/scratch13/acasais/second/task1/reco-500runs.p', 'wb') as p:
#     pickle.dump(reco, p)
  


       





