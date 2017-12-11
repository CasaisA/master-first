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
t1 = TTree('pi-e_truth','pi-e_truth')
t3 = TTree('kS0_truth','kS0_truth')
t4 = TTree('pi-e_reco','pi-e_reco')
t2 = TTree('ks0products_reco','ks0products_reco')


truthd = {]#non fai falla xa ... 
ks0_recod = {}
ks0d = {}
recod ={}
#t1
truthd_px=np.zeros(1,dtype=float)
truthd_py=np.zeros(1,dtype=float)
truthd_pz=np.zeros(1,dtype=float)
truthd_pT=np.zeros(1,dtype=float)
truthd_p=np.zeros(1,dtype=float)
truthd_eta=np.zeros(1,dtype=float)
truthd_phi=np.zeros(1,dtype=float)
truthd_pid=np.zeros(1,dtype=float)
truthd_evtid = np.zeros(1,dtype=float)
truthd_runid=np.zeros(1,dtype=float)

t1.Branch('evt_id',truthd_evtid,'evt_id/D')
t1.Branch('run_id',truthd_runid,'run_id/D')
t1.Branch('px',truthd_px,'px/D')
t1.Branch('py',truthd_py,'py/D')
t1.Branch('pz',truthd_pz,'pz/D')
t1.Branch('p',truthd_p,'p/D')
t1.Branch('pT',truthd_pT,'pT/D')
t1.Branch('eta',truthd_eta,'eta/D')
t1.Branch('phi',truthd_phi,'phi/D')
t1.Branch('pid',truthd_pid,'pid/D')
#t3
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
ks0d['eminus_px']=np.zeros(1,dtype=float)
ks0d['eminus_py']=np.zeros(1,dtype=float)
ks0d['eminus_pz']=np.zeros(1,dtype=float)
ks0d['eminus_pT']=np.zeros(1,dtype=float)
ks0d['eminus_p']=np.zeros(1,dtype=float)
ks0d['eminus_eta']=np.zeros(1,dtype=float)
ks0d['eminus_phi']=np.zeros(1,dtype=float)
ks0d['piminus_px']=np.zeros(1,dtype=float)
ks0d['piminus_py']=np.zeros(1,dtype=float)
ks0d['piminus_pz']=np.zeros(1,dtype=float)
ks0d['piminus_pT']=np.zeros(1,dtype=float)
ks0d['piminus_p']=np.zeros(1,dtype=float)
ks0d['piminus_eta']=np.zeros(1,dtype=float)
ks0d['piminus_phi']=np.zeros(1,dtype=float)

ks0d['eplus_px']=np.zeros(1,dtype=float)
ks0d['eplus_py']=np.zeros(1,dtype=float)
ks0d['eplus_pz']=np.zeros(1,dtype=float)
ks0d['eplus_pT']=np.zeros(1,dtype=float)
ks0d['eplus_p']=np.zeros(1,dtype=float)
ks0d['eplus_eta']=np.zeros(1,dtype=float)
ks0d['eplus_phi']=np.zeros(1,dtype=float)
ks0d['piplus_px']=np.zeros(1,dtype=float)
ks0d['piplus_py']=np.zeros(1,dtype=float)
ks0d['piplus_pz']=np.zeros(1,dtype=float)
ks0d['piplus_pT']=np.zeros(1,dtype=float)
ks0d['piplus_p']=np.zeros(1,dtype=float)
ks0d['piplus_eta']=np.zeros(1,dtype=float)
ks0d['piplus_phi']=np.zeros(1,dtype=float)

t3.Branch('evt_id',ks0d['evt_id'],'evt_id/D')
t3.Branch('run_id',ks0d['run_id'],'run_id/D')
t3.Branch('px',ks0d['px'],'px/D')
t3.Branch('py',ks0d['py'],'py/D')
t3.Branch('pz',ks0d['pz'],'pz/D')
t3.Branch('p',ks0dd['p'],'p/D')
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



#t2


ks0_recod['evt_id']=np.zeros(1,dtype=float)
ks0_recod['run_id']=np.zeros(1,dtype=float)

ks0_recod['eminus_px']=np.zeros(1,dtype=float)
ks0_recod['eminus_py']=np.zeros(1,dtype=float)
ks0_recod['eminus_pz']=np.zeros(1,dtype=float)
ks0_recod['eminus_p']=np.zeros(1,dtype=float)
ks0_recod['eminus_pT']=np.zeros(1,dtype=float)
ks0_recod['eminus_eta']=np.zeros(1,dtype=float)
ks0_recod['eminus_phi']=np.zeros(1,dtype=float)
ks0_recod['eminus_trck_type']=np.zeros(1,dtype=float)

ks0_recod['eplus_px']=np.zeros(1,dtype=float)
ks0_recod['eplus_py']=np.zeros(1,dtype=float)
ks0_recod['eplus_pz']=np.zeros(1,dtype=float)
ks0_recod['eplus_p']=np.zeros(1,dtype=float)
ks0_recod['eplus_pT']=np.zeros(1,dtype=float)
ks0_recod['eplus_eta']=np.zeros(1,dtype=float)
ks0_recod['eplus_phi']=np.zeros(1,dtype=float)
ks0_recod['eplus_trck_type']=np.zeros(1,dtype=float)

ks0_recod['piminus_px']=np.zeros(1,dtype=float)
ks0_recod['piminus_py']=np.zeros(1,dtype=float)
ks0_recod['piminus_pz']=np.zeros(1,dtype=float)
ks0_recod['piminus_p']=np.zeros(1,dtype=float)
ks0_recod['piminus_pT']=np.zeros(1,dtype=float)
ks0_recod['piminus_eta']=np.zeros(1,dtype=float)
ks0_recod['piminus_phi']=np.zeros(1,dtype=float)
ks0_recod['piminus_trck_type']=np.zeros(1,dtype=float)

ks0_recod['piplus_px']=np.zeros(1,dtype=float)
ks0_recod['piplus_py']=np.zeros(1,dtype=float)
ks0_recod['piplus_pz']=np.zeros(1,dtype=float)
ks0_recod['piplus_p']=np.zeros(1,dtype=float)
ks0_recod['piplus_pT']=np.zeros(1,dtype=float)
ks0_recod['piplus_eta']=np.zeros(1,dtype=float)
ks0_recod['piplus_phi']=np.zeros(1,dtype=float)
ks0_recod['piplus_trck_type']=np.zeros(1,dtype=float)


t2.Branch('evt_id',ks0_recod['evt_id'],'evt_id/D')
t2.Branch('run_id',ks0_recod['run_id'],'run_id/D')


t2.Branch('eminus_px',ks0_recod['eminus_px'],'eminus_px/D')
t2.Branch('eminus_py',ks0_recod['eminus_py'],'eminus_py/D')
t2.Branch('eminus_pz',ks0_recod['eminus_pz'],'eminus_pz/D')
t2.Branch('eminus_pT',ks0_recod['eminus_pT'],'eminus_pT/D')
t2.Branch('eminus_p',ks0_recod['eminus_p'],'eminus_p/D')

t2.Branch('eplus_px',ks0_recod['eplus_px'],'eplus_px/D')
t2.Branch('eplus_py',ks0_recod['eplus_py'],'eplus_py/D')
t2.Branch('eplus_pz',ks0_recod['eplus_pz'],'eplus_pz/D')
t2.Branch('eplus_pT',ks0_recod['eplus_pT'],'eplus_pT/D')
t2.Branch('eplus_p',ks0_recod['eplus_p'],'eplus_p/D')

t2.Branch('piminus_px',ks0_recod['piminus_px'],'piminus_px/D')
t2.Branch('piminus_py',ks0_recod['piminus_py'],'piminus_py/D')
t2.Branch('piminus_pz',ks0_recod['piminus_pz'],'piminus_pz/D')
t2.Branch('piminus_pT',ks0_recod['piminus_pT'],'piminus_pT/D')
t2.Branch('piminus_p',ks0_recod['piminus_p'],'piminus_p/D')

t2.Branch('piplus_px',ks0_recod['piplus_px'],'piplus_px/D')
t2.Branch('piplus_py',ks0_recod['piplus_py'],'piplus_py/D')
t2.Branch('piplus_pz',ks0_recod['piplus_pz'],'piplus_pz/D')
t2.Branch('piplus_pT',ks0_recod['piplus_pT'],'piplus_pT/D')
t2.Branch('piplus_p',ks0_recod['piplus_p'],'piplus_p/D')

#t4

recod_px=np.zeros(1,dtype=float)
recod_py=np.zeros(1,dtype=float)
recod_pz=np.zeros(1,dtype=float)
recod_pT=np.zeros(1,dtype=float)
recod_p=np.zeros(1,dtype=float)
recod_eta=np.zeros(1,dtype=float)
recod_phi=np.zeros(1,dtype=float)

recod_px_truth=np.zeros(1,dtype=float)
recod_py_truth=np.zeros(1,dtype=float)
recod_pz_truth=np.zeros(1,dtype=float)
recod_pT_truth=np.zeros(1,dtype=float)
recod_p_truth=np.zeros(1,dtype=float)
recod_eta_truth=np.zeros(1,dtype=float)
recod_phi_truth=np.zeros(1,dtype=float)

recod_pid=np.zeros(1,dtype=float)
recod_evtid = np.zeros(1,dtype=float)
recod_runid=np.zeros(1,dtype=float)
recod_trck_type=np.zeros(1,dtype=float)

t4.Branch('evt_id',recod_evtid,'evt_id/D')
t4.Branch('run_id',recod_runid,'run_id/D')
t4.Branch('px',recod_px,'px/D')
t4.Branch('py',recod_py,'py/D')
t4.Branch('pz',recod_pz,'pz/D')
t4.Branch('p',recod_p,'p/D')
t4.Branch('pT',recod_pT,'pT/D')
t4.Branch('eta',recod_eta,'eta/D')
t4.Branch('phi',recod_phi,'phi/D')

t4.Branch('px_truth',recod_px,'px/D')
t4.Branch('py_truth',recod_py,'py/D')
t4.Branch('pz_truth',recod_pz,'pz/D')
t4.Branch('p_truth',recod_p,'p/D')
t4.Branch('pT_truth',recod_pT,'pT/D')
t4.Branch('eta_truth',recod_eta,'eta/D')
t4.Branch('phi_truth',recod_phi,'phi/D')



t4.Branch('pid',recod_pid,'pid/D')
t4.Branch('trck_type',recod_trck_type,'trck_type/D')





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
    #nesta lista vou a meter os keys dos ks0 que atope
    #ks0_keys = []
    mother_key = 0
    products_keys_pipiee = []
    for particle in mcparticles:
	    #tipicas sentencias para evitar que unha particula corrupta entre no bucle
	    if not particle: continue
	    if not particle.momentum(): continue
	    if not len(particle.momentum()): continue
            products = map(lambda x: x,particle.endVertices()[-1].products())
	    products = filter(lambda x: abs(x.particleID().pid())==11 or abs(x.particleID().pid())==211,products)
	    products_pid = map(lambda x: x.particleID().pid(),products)
	    
	    
	    if particle.particleID().pid()==310 and (11 in products_pid) and (-11 in products_pid) and (211 in products_pid) and (-211 in products_pid):
		    #ks0_keys.append(particle.key())
		    #nesta lista van estar os keys dos pions e electrons asociados a este ks0
		    products_keys_pipiee.append(map(lambda x: x.key(),products))
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
		    for product in products:
			    if product.particleID.pid()==11:
				    ks0d['eminus_px'][0]=product.momentum().x()
				    ks0d['eminus_py'][0]=product.momentum().y()
				    ks0d['eminus_pz'][0]=product.momentum().z()
				    ks0d['eminus_pT'][0]=product.pt()
				    ks0d['eminus_p'][0]=product.p()
				    ks0d['eminus_eta'][0]=product.momentum().eta()
				    ks0d['eminus_phi'][0]=product.momentum().phi()
			    if product.particleID.pid()==-11:
				    ks0d['eplus_px'][0]=product.momentum().x()
				    ks0d['eplus_py'][0]=product.momentum().y()
				    ks0d['eplus_pz'][0]=product.momentum().z()
				    ks0d['eplus_pT'][0]=product.pt()
				    ks0d['eplus_p'][0]=product.p()
				    ks0d['eplus_eta'][0]=product.momentum().eta()
				    ks0d['eplus_phi'][0]=product.momentum().phi()
			    if product.particleID.pid()==-211
				    ks0d['piminus_px'][0]=product.momentum().x()
				    ks0d['piminus_py'][0]=product.momentum().y()
				    ks0d['piminus_pz'][0]=product.momentum().z()
				    ks0d['piminus_pT'][0]=product.pt()
				    ks0d['piminus_p'][0]=product.p()
				    ks0d['piminus_eta'][0]=product.momentum().eta()
				    ks0d['piminus_phi'][0]=product.momentum().phi()
			    if product.particleID.pid()==211:
				    ks0d['piplus_px'][0]=product.momentum().x()
				    ks0d['piplus_py'][0]=product.momentum().y()
				    ks0d['piplus_pz'][0]=product.momentum().z()
				    ks0d['piplus_pT'][0]=product.pt()
				    ks0d['piplus_p'][0]=product.p()
				    ks0d['piplus_eta'][0]=product.momentum().eta()
				    ks0d['piplus_phi'][0]=product.momentum().phi()
		    
		    t3.Fill()

		    cks0+=1
		    if not cks0%100:
			    t3.AutoSave()
		    
	    
			    
	    	    
	    if abs(particle.particleID().pid())==11 or abs(particle.particleID().pid())==211
		    truthd_px[0]=particle.momentum().x()
		    truthd_py[0]=particle.momentum().y()
		    truthd_pz[0]=particle.momentum().z()
		    truthd_pT[0]=particle.pt()
		    truthd_p[0]=particle.p()
		    truthd_eta[0]=particle.momentum().eta()
		    truthd_phi[0]=particle.momentum().phi()
		    truthd_pid[0]=particle.particleID().pid()
		    truthd_evtid[0] = TES['Rec/Header'].evtNumber()
		    truthd_runid[0]= TES['Rec/Header'].runNumber()
		    t1.Fill()
		    ctruth+=1
		    if not ctruth%100:
			    
			    t1.AutoSave()

		    
	    
    for proto in myprotos:
	    
	    track = proto.track()
	    mcpar = get_mcpar(proto)
	    if mcpar == 0: continue
	    mother = mcpar.mother()
	    if not mother: continue
	    if not len(mother.momentum()): continue
	    
	    if abs(mcpar.particleID.pid())==11 or abs(mcpar.particleID.pid())==211:
		    recod_px[0]=track.momentum().x()
		    recod_py[0]=track.momentum().y()
		    recod_pz[0]=track.momentum().z()
		    recod_pT[0]=track.pt()
		    recod_p[0]=track.p()
		    recod_eta[0]=track.momentum().eta()
		    recod_phi[0]=track.momentum().phi()
		    recod_pid[0]=mcpar.particleID().pid()
		    
		    recod_px_truth[0]=mcpar.momentum().x()
		    recod_py_truth[0]=mcpar.momentum().y()
		    recod_pz_truth[0]=mcpar.momentum().z()
		    recod_pT_truth[0]=mcpar.pt()
		    recod_p_truth[0]=mcpar.p()
		    recod_eta_truth[0]=mcpar.momentum().eta()
		    recod_phi_truth[0]=mcpar.momentum().phi()
		    


		    
		    recod_evtid[0] = TES['Rec/Header'].evtNumber()
		    recod_runid[0]= TES['Rec/Header'].runNumber()
		    recod_trck_type[0]=track.type()
		    t4.Fill()
		    creco+=1
		    if not creco%100:
			    t4.AutoSave()



    protos_good = filter(lambda x: mcpar(x)!=0,myprotos)
    #parts_proto = map(lambda x: mcpar(x),protos_good)
    
    proto_keys = map(lambda x: mcpar(x).key(),protos_good)
    #ks0_reconstructed = False
    for index in xrange(len(products_keys_pipiee)):
	    
	    if all(x in proto_keys for x in products_keys_pipiee[index]):
		    protos_temp = filter(lambda x: mcpar(x).key() in products_keys_pipiee[index],protos_good)
		    #parts_proto_temp = map(lambda x: mcpar(x),protos_temp)
		    #tracks_proto_temp=map(lambda x: x.track(),protos_temp)
		    for ks0proto in protos_temp:
			    ks0par = mcpar(ks0proto)
			    ks0track = ks0proto.track()
			    ks0_reco['evt_id']=TES['Rec/Header'].evtNumber()
			    ks0_reco['run_id']=TES['Rec/Header'].runNumber()
			    if ks0par.particleID().pid()==11:
				    
				    ks0_recod['eminus_px'][0]=ks0track.momentum().x()
				    ks0_recod['eminus_py'][0]=ks0track.momentum().y()
				    ks0_recod['eminus_pz'][0]=ks0track.momentum().z()
				    ks0_recod['eminus_p'][0]=ks0track.p()
				    ks0_recod['eminus_pT'][0]ks0track.pt()
				    ks0_recod['eminus_eta'][0]=ks0track.momentum().eta()
				    ks0_recod['eminus_phi'][0]=ks0track.momentum().phi()
				    ks0_recod['eminus_trck_type']=ks0track.type()

			    if ks0par.particleID().pid()==-11
				    
				    ks0_recod['eplus_px'][0]=ks0track.momentum().x()
				    ks0_recod['eplus_py'][0]=ks0track.momentum().y()
				    ks0_recod['eplus_pz'][0]=ks0track.momentum().z()
				    ks0_recod['eplus_p'][0]=ks0track.p()
				    ks0_recod['eplus_pT'][0]ks0track.pt()
				    ks0_recod['eplus_eta'][0]=ks0track.momentum().eta()
				    ks0_recod['eplus_phi'][0]=ks0track.momentum().phi()
				    ks0_recod['eplus_trck_type']=ks0track.type()
			    if ks0par.particleID().pid()==211:
				    
				    ks0_recod['piplus_px'][0]=ks0track.momentum().x()
				    ks0_recod['piplus_py'][0]=ks0track.momentum().y()
				    ks0_recod['piplus_pz'][0]=ks0track.momentum().z()
				    ks0_recod['piplus_p'][0]=ks0track.p()
				    ks0_recod['piplus_pT'][0]ks0track.pt()
				    ks0_recod['piplus_eta'][0]=ks0track.momentum().eta()
				    ks0_recod['piplus_phi'][0]=ks0track.momentum().phi()
				    ks0_recod['piplus_trck_type']=ks0track.type()


			    if ks0par.particleID().pid()==-211:
				    
				    ks0_recod['piminus_px'][0]=ks0track.momentum().x()
				    ks0_recod['piminus_py'][0]=ks0track.momentum().y()
				    ks0_recod['piminus_pz'][0]=ks0track.momentum().z()
				    ks0_recod['piminus_p'][0]=ks0track.p()
				    ks0_recod['piminus_pT'][0]ks0track.pt()
				    ks0_recod['piminus_eta'][0]=ks0track.momentum().eta()
				    ks0_recod['piminus_phi'][0]=ks0track.momentum().phi()
				    ks0_recod['eminus_trck_type']=ks0track.type()
	
			    
			    t2.Fill()

f1.cd()	
f1.Write()
f1.Close()	
# with open('/scratch13/acasais/second/task1/truth-500runs.p', 'wb') as f:
#     pickle.dump(mctruth, f)

# with open('/scratch13/acasais/second/task1/reco-500runs.p', 'wb') as p:
#     pickle.dump(reco, p)
  


       





