#! /usr/bin/env python

## CONFIGURE DAVINCI (GENERAL CONFIGURATION OF THE JOB)
from Configurables import DaVinci, ChargedPP2MC, ChargedProtoParticleMaker
import GaudiPython
from Gaudi.Configuration import *
import pandas as pd
import math as m

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
magnet= str(sys.argv[3])
dst_file = []
for i in xrange(1,71):
        i = str(i)
	if magnet=='up':
		if int(i)<10:
			dst_file_name = '/scratch29/KsPiPiee/'+magnet+'00037694_0000000'+i+'_1.allstreams.dst'
		else:
			dst_file_name = '/scratch29/KsPiPiee/'+magnet+'/00037694_000000'+i+'_1.allstreams.dst'
	if magnet =='down':
		if int(i)<10:
			dst_file_name = '/scratch29/KsPiPiee/'+magnet+'00037700_0000000'+i+'_1.allstreams.dst'
		else:
			dst_file_name = '/scratch29/KsPiPiee/'+magnet+'/00037700_000000'+i+'_1.allstreams.dst'
		
        if os.path.isfile(dst_file_name):
                dst_file.append(dst_file_name)

if magnet=='down':
	dst_file.append('/scratch29/KsPiPiee/down/MC_2012_34124015_Beam4000GeV2012MagDownNu2.5Pythia8_Sim08e_Digi13_Trig0x409f0045_Reco14a_Stripping20NoPrescalingFlagged_ALLSTREAMS.dst')

DaVinci().Input = dst_file

f1 = TFile('/scratch13/acasais/second/KsPiPiee-root/KsPiPiee_'+magnet+'_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'.root','recreate')
#t1 = TTree('pi-e_truth','pi-e_truth')
t3 = TTree('kS0_truth','kS0_truth')
t4 = TTree('pi-e_reco','pi-e_reco')
t2 = TTree('ks0products_reco','ks0products_reco')



# #t1
# truthd_px=np.zeros(1,dtype=float)
# truthd_py=np.zeros(1,dtype=float)
# truthd_pz=np.zeros(1,dtype=float)
# truthd_pT=np.zeros(1,dtype=float)
# truthd_p=np.zeros(1,dtype=float)
# truthd_eta=np.zeros(1,dtype=float)
# truthd_phi=np.zeros(1,dtype=float)
# truthd_pid=np.zeros(1,dtype=float)
# truthd_evtid = np.zeros(1,dtype=float)
# truthd_runid=np.zeros(1,dtype=float)

# t1.Branch('evt_id',truthd_evtid,'evt_id/D')
# t1.Branch('run_id',truthd_runid,'run_id/D')
# t1.Branch('px',truthd_px,'px/D')
# t1.Branch('py',truthd_py,'py/D')
# t1.Branch('pz',truthd_pz,'pz/D')
# t1.Branch('p',truthd_p,'p/D')
# t1.Branch('pT',truthd_pT,'pT/D')
# t1.Branch('eta',truthd_eta,'eta/D')
# t1.Branch('phi',truthd_phi,'phi/D')
# t1.Branch('pid',truthd_pid,'pid/D')
#t3

ks0d_evt_id=np.zeros(1,dtype=float)
ks0d_run_id=np.zeros(1,dtype=float)
ks0d_px=np.zeros(1,dtype=float)
ks0d_py=np.zeros(1,dtype=float)
ks0d_pz=np.zeros(1,dtype=float)
ks0d_pT=np.zeros(1,dtype=float)
ks0d_p=np.zeros(1,dtype=float)
ks0d_eta=np.zeros(1,dtype=float)
ks0d_phi=np.zeros(1,dtype=float)
ks0d_pid=np.zeros(1,dtype=float)
ks0d_PV_x=np.zeros(1,dtype=float)
ks0d_PV_y=np.zeros(1,dtype=float)
ks0d_PV_z=np.zeros(1,dtype=float)
ks0d_SV_x=np.zeros(1,dtype=float)
ks0d_SV_y=np.zeros(1,dtype=float)
ks0d_SV_z=np.zeros(1,dtype=float)
ks0d_eminus_px=np.zeros(1,dtype=float)
ks0d_eminus_py=np.zeros(1,dtype=float)
ks0d_eminus_pz=np.zeros(1,dtype=float)
ks0d_eminus_pT=np.zeros(1,dtype=float)
ks0d_eminus_p=np.zeros(1,dtype=float)
ks0d_eminus_eta=np.zeros(1,dtype=float)
ks0d_eminus_phi=np.zeros(1,dtype=float)
ks0d_piminus_px=np.zeros(1,dtype=float)
ks0d_piminus_py=np.zeros(1,dtype=float)
ks0d_piminus_pz=np.zeros(1,dtype=float)
ks0d_piminus_pT=np.zeros(1,dtype=float)
ks0d_piminus_p=np.zeros(1,dtype=float)
ks0d_piminus_eta=np.zeros(1,dtype=float)
ks0d_piminus_phi=np.zeros(1,dtype=float)

ks0d_eplus_px=np.zeros(1,dtype=float)
ks0d_eplus_py=np.zeros(1,dtype=float)
ks0d_eplus_pz=np.zeros(1,dtype=float)
ks0d_eplus_pT=np.zeros(1,dtype=float)
ks0d_eplus_p=np.zeros(1,dtype=float)
ks0d_eplus_eta=np.zeros(1,dtype=float)
ks0d_eplus_phi=np.zeros(1,dtype=float)
ks0d_piplus_px=np.zeros(1,dtype=float)
ks0d_piplus_py=np.zeros(1,dtype=float)
ks0d_piplus_pz=np.zeros(1,dtype=float)
ks0d_piplus_pT=np.zeros(1,dtype=float)
ks0d_piplus_p=np.zeros(1,dtype=float)
ks0d_piplus_eta=np.zeros(1,dtype=float)
ks0d_piplus_phi=np.zeros(1,dtype=float)

t3.Branch('evt_id',ks0d_evt_id,'evt_id/D')
t3.Branch('run_id',ks0d_run_id,'run_id/D')
t3.Branch('px',ks0d_px,'px/D')
t3.Branch('py',ks0d_py,'py/D')
t3.Branch('pz',ks0d_pz,'pz/D')
t3.Branch('p',ks0d_p,'p/D')
t3.Branch('pT',ks0d_pT,'pT/D')
t3.Branch('eta',ks0d_eta,'eta/D')
t3.Branch('phi',ks0d_phi,'phi/D')
t3.Branch('pid',ks0d_pid,'pid/D')
t3.Branch('PV_x',ks0d_PV_x,'PV_x/D')
t3.Branch('PV_y',ks0d_PV_y,'PV_y/D')
t3.Branch('PV_z',ks0d_PV_z,'PV_z/D')
t3.Branch('SV_x',ks0d_SV_x,'SV_x/D')
t3.Branch('SV_y',ks0d_SV_y,'SV_y/D')
t3.Branch('SV_z',ks0d_SV_z,'SV_z/D')

t3.Branch('eminus_px',ks0d_eminus_px,'eminus_px/D')
t3.Branch('eminus_py',ks0d_eminus_py,'eminus_py/D')
t3.Branch('eminus_pz',ks0d_eminus_pz,'eminus_pz/D')
t3.Branch('eminus_pT',ks0d_eminus_pT,'eminus_pT/D')
t3.Branch('eminus_p',ks0d_eminus_p,'eminus_p/D')
t3.Branch('eminus_eta',ks0d_eminus_eta,'eminus_eta/D')
t3.Branch('eminus_phi',ks0d_eminus_phi,'eminus_phi/D')

t3.Branch('piminus_px',ks0d_piminus_px,'piminus_px/D')
t3.Branch('piminus_py',ks0d_piminus_py,'piminus_py/D')
t3.Branch('piminus_pz',ks0d_piminus_pz,'piminus_pz/D')
t3.Branch('piminus_pT',ks0d_piminus_pT,'piminus_pT/D')
t3.Branch('piminus_p',ks0d_piminus_p,'piminus_p/D')
t3.Branch('piminus_eta',ks0d_piminus_eta,'piminus_eta/D')
t3.Branch('piminus_phi',ks0d_piminus_phi,'piminus_phi/D')

t3.Branch('eplus_px',ks0d_eplus_px,'eplus_px/D')
t3.Branch('eplus_py',ks0d_eplus_py,'eplus_py/D')
t3.Branch('eplus_pz',ks0d_eplus_pz,'eplus_pz/D')
t3.Branch('eplus_pT',ks0d_eplus_pT,'eplus_pT/D')
t3.Branch('eplus_p',ks0d_eplus_p,'eplus_p/D')
t3.Branch('eplus_eta',ks0d_eplus_eta,'eplus_eta/D')
t3.Branch('eplus_phi',ks0d_eplus_phi,'eplus_phi/D')

t3.Branch('piplus_px',ks0d_piplus_px,'piplus_px/D')
t3.Branch('piplus_py',ks0d_piplus_py,'piplus_py/D')
t3.Branch('piplus_pz',ks0d_piplus_pz,'piplus_pz/D')
t3.Branch('piplus_pT',ks0d_piplus_pT,'piplus_pT/D')
t3.Branch('piplus_p',ks0d_piplus_p,'piplus_p/D')
t3.Branch('piplus_eta',ks0d_piplus_eta,'piplus_eta/D')
t3.Branch('piplus_phi',ks0d_piplus_phi,'piplus_phi/D')



#t2
ks0_recod_evt_id=np.zeros(1,dtype=float)
ks0_recod_run_id=np.zeros(1,dtype=float)

ks0_recod_px_truth=np.zeros(1,dtype=float)
ks0_recod_py_truth=np.zeros(1,dtype=float)
ks0_recod_pz_truth=np.zeros(1,dtype=float)
ks0_recod_pT_truth=np.zeros(1,dtype=float)
ks0_recod_p_truth=np.zeros(1,dtype=float)
ks0_recod_eta_truth=np.zeros(1,dtype=float)
ks0_recod_phi_truth=np.zeros(1,dtype=float)

ks0_recod_PV_x_truth=np.zeros(1,dtype=float)
ks0_recod_PV_y_truth=np.zeros(1,dtype=float)
ks0_recod_PV_z_truth=np.zeros(1,dtype=float)
ks0_recod_SV_x_truth=np.zeros(1,dtype=float)
ks0_recod_SV_y_truth=np.zeros(1,dtype=float)
ks0_recod_SV_z_truth=np.zeros(1,dtype=float)





ks0_recod_eminus_px=np.zeros(1,dtype=float)
ks0_recod_eminus_py=np.zeros(1,dtype=float)
ks0_recod_eminus_pz=np.zeros(1,dtype=float)
ks0_recod_eminus_p=np.zeros(1,dtype=float)
ks0_recod_eminus_pT=np.zeros(1,dtype=float)
ks0_recod_eminus_eta=np.zeros(1,dtype=float)
ks0_recod_eminus_phi=np.zeros(1,dtype=float)
ks0_recod_eminus_trck_type=np.zeros(1,dtype=float)




ks0_recod_eplus_px=np.zeros(1,dtype=float)
ks0_recod_eplus_py=np.zeros(1,dtype=float)
ks0_recod_eplus_pz=np.zeros(1,dtype=float)
ks0_recod_eplus_p=np.zeros(1,dtype=float)
ks0_recod_eplus_pT=np.zeros(1,dtype=float)
ks0_recod_eplus_eta=np.zeros(1,dtype=float)
ks0_recod_eplus_phi=np.zeros(1,dtype=float)
ks0_recod_eplus_trck_type=np.zeros(1,dtype=float)

ks0_recod_piminus_px=np.zeros(1,dtype=float)
ks0_recod_piminus_py=np.zeros(1,dtype=float)
ks0_recod_piminus_pz=np.zeros(1,dtype=float)
ks0_recod_piminus_p=np.zeros(1,dtype=float)
ks0_recod_piminus_pT=np.zeros(1,dtype=float)
ks0_recod_piminus_eta=np.zeros(1,dtype=float)
ks0_recod_piminus_phi=np.zeros(1,dtype=float)
ks0_recod_piminus_trck_type=np.zeros(1,dtype=float)

ks0_recod_piplus_px=np.zeros(1,dtype=float)
ks0_recod_piplus_py=np.zeros(1,dtype=float)
ks0_recod_piplus_pz=np.zeros(1,dtype=float)
ks0_recod_piplus_p=np.zeros(1,dtype=float)
ks0_recod_piplus_pT=np.zeros(1,dtype=float)
ks0_recod_piplus_eta=np.zeros(1,dtype=float)
ks0_recod_piplus_phi=np.zeros(1,dtype=float)
ks0_recod_piplus_trck_type=np.zeros(1,dtype=float)


t2.Branch('evt_id',ks0_recod_evt_id,'evt_id/D')
t2.Branch('run_id',ks0_recod_run_id,'run_id/D')

t2.Branch('px_truth',ks0_recod_px_truth,'px_truth/D')
t2.Branch('py_truth',ks0_recod_py_truth,'py_truth/D')
t2.Branch('pz_truth',ks0_recod_pz_truth,'pz_truth/D')

t2.Branch('p_truth',ks0_recod_p_truth,'p_truth/D')
t2.Branch('pT_truth',ks0_recod_pT_truth,'pT_truth/D')
t2.Branch('phi_truth',ks0_recod_phi_truth,'phi_truth/D')
t2.Branch('eta_truth',ks0_recod_eta_truth,'eta_truth/D')
t2.Branch('PV_x',ks0_recod_PV_x_truth,'PV_x/D')
t2.Branch('PV_y',ks0_recod_PV_y_truth,'PV_y/D')
t2.Branch('PV_z',ks0_recod_PV_z_truth,'PV_z/D')

t2.Branch('SV_x',ks0_recod_SV_x_truth,'SV_x/D')
t2.Branch('SV_y',ks0_recod_SV_y_truth,'SV_y/D')
t2.Branch('SV_z',ks0_recod_SV_z_truth,'SV_z/D')

t2.Branch('eminus_px',ks0_recod_eminus_px,'eminus_px/D')
t2.Branch('eminus_py',ks0_recod_eminus_py,'eminus_py/D')
t2.Branch('eminus_pz',ks0_recod_eminus_pz,'eminus_pz/D')
t2.Branch('eminus_pT',ks0_recod_eminus_pT,'eminus_pT/D')
t2.Branch('eminus_p',ks0_recod_eminus_p,'eminus_p/D')
t2.Branch('eminus_trck_type',ks0_recod_eminus_trck_type,'eminus_trck_type/D')

t2.Branch('eplus_px',ks0_recod_eplus_px,'eplus_px/D')
t2.Branch('eplus_py',ks0_recod_eplus_py,'eplus_py/D')
t2.Branch('eplus_pz',ks0_recod_eplus_pz,'eplus_pz/D')
t2.Branch('eplus_pT',ks0_recod_eplus_pT,'eplus_pT/D')
t2.Branch('eplus_p',ks0_recod_eplus_p,'eplus_p/D')
t2.Branch('eplus_trck_type',ks0_recod_eplus_trck_type,'eplus_trck_type/D')

t2.Branch('piminus_px',ks0_recod_piminus_px,'piminus_px/D')
t2.Branch('piminus_py',ks0_recod_piminus_py,'piminus_py/D')
t2.Branch('piminus_pz',ks0_recod_piminus_pz,'piminus_pz/D')
t2.Branch('piminus_pT',ks0_recod_piminus_pT,'piminus_pT/D')
t2.Branch('piminus_p',ks0_recod_piminus_p,'piminus_p/D')
t2.Branch('piminus_trck_type',ks0_recod_piminus_trck_type,'piminus_trck_type/D')

t2.Branch('piplus_px',ks0_recod_piplus_px,'piplus_px/D')
t2.Branch('piplus_py',ks0_recod_piplus_py,'piplus_py/D')
t2.Branch('piplus_pz',ks0_recod_piplus_pz,'piplus_pz/D')
t2.Branch('piplus_pT',ks0_recod_piplus_pT,'piplus_pT/D')
t2.Branch('piplus_p',ks0_recod_piplus_p,'piplus_p/D')
t2.Branch('piplus_trck_type',ks0_recod_piplus_trck_type,'piplus_trck_type/D')
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

t4.Branch('px_truth',recod_px_truth,'px_truth/D')
t4.Branch('py_truth',recod_py_truth,'py_truth/D')
t4.Branch('pz_truth',recod_pz_truth,'pz_truth/D')
t4.Branch('p_truth',recod_p_truth,'p_truth/D')
t4.Branch('pT_truth',recod_pT_truth,'pT_truth/D')
t4.Branch('eta_truth',recod_eta_truth,'eta_truth/D')
t4.Branch('phi_truth',recod_phi_truth,'phi_truth/D')



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

## GET MCPAR FROM PROTO
def get_mcpar(proto):
    LinkRef = GaudiPython.gbl.LHCb.LinkReference()
    linker = TES["Link/Rec/ProtoP/MyProtoParticles/PP2MC"]
    ok = linker.firstReference(proto.key(), None ,LinkRef)
    if not ok: return 0
    return TES["MC/Particles"][LinkRef.objectKey()]


ctruth=0
creco= 0
cks0t=0
cks0r=0
counter = 0
#RANGE IS AS BIG AS YOU WANT IT TO BE
if int(sys.argv[1])>1: 
	gaudi.run(int(sys.argv[1])-1)
for i in range(int(sys.argv[2])-int(sys.argv[1])+1):
    #f1.cd()
    counter+=1
    c1 = gaudi.run(1)
    tracks = TES["Rec/Track/Best"]
    mcparticles = TES["MC/Particles"]
    myprotos = TES["Rec/ProtoP/MyProtoParticles"]
    
    mother_key = 0
    products_keys_pipiee = []
    mcparticles = filter(lambda x: x,mcparticles)
    mcparticles = filter(lambda x: x.momentum(),mcparticles)
    mcparticles = filter(lambda x: len(x.endVertices()),mcparticles)
    mcparticles = filter(lambda x: x.particleID().pid()==310,mcparticles)
    mcparticles = filter(lambda x: all([i in map(lambda y: y.particleID().pid(),x.endVertices()[-1].products()) for i in [11,-11,211,-211]]),mcparticles)
    for particle in mcparticles:
	    
            products = map(lambda x: x,particle.endVertices()[-1].products())
	    products = filter(lambda x: abs(x.particleID().pid())==11 or abs(x.particleID().pid())==211,products)
	    products_pid = map(lambda x: x.particleID().pid(),products)
	    
	    
	    
	    #nesta lista van estar os keys dos pions e electrons asociados a este ks0
	    products_keys_pipiee.append(map(lambda x: x.key(),products))
	    ks0d_evt_id[0]= TES['Rec/Header'].evtNumber()
	    ks0d_run_id[0]= TES['Rec/Header'].runNumber()
	    ks0d_px[0]=particle.momentum().x()
	    ks0d_py[0]=particle.momentum().y()
	    ks0d_pz[0]=particle.momentum().z()
	    ks0d_p[0]=particle.p()
	    ks0d_pT[0]=particle.pt()
	    ks0d_eta[0]=particle.momentum().eta()
	    ks0d_phi[0]=particle.momentum().phi()
	    ks0d_pid[0]=particle.particleID().pid()
	    ks0d_PV_x[0]=particle.originVertex().position().x()
	    ks0d_PV_y[0]=particle.originVertex().position().y()
	    ks0d_PV_z[0]=particle.originVertex().position().z()
	    ks0d_SV_x[0]=particle.endVertices()[-1].position().x()
	    ks0d_SV_y[0]=particle.endVertices()[-1].position().y()
	    ks0d_SV_z[0]=particle.endVertices()[-1].position().z()
	    for product in products:
	    
	          if product.particleID().pid()==11:
			  ks0d_eminus_px[0]=product.momentum().x()
			  ks0d_eminus_py[0]=product.momentum().y()
			  ks0d_eminus_pz[0]=product.momentum().z()
			  ks0d_eminus_pT[0]=product.pt()
			  ks0d_eminus_p[0]=product.p()
			  ks0d_eminus_eta[0]=product.momentum().eta()
			  ks0d_eminus_phi[0]=product.momentum().phi()
		  if product.particleID().pid()==-11:
			  ks0d_eplus_px[0]=product.momentum().x()
			  ks0d_eplus_py[0]=product.momentum().y()
			  ks0d_eplus_pz[0]=product.momentum().z()
			  ks0d_eplus_pT[0]=product.pt()
			  ks0d_eplus_p[0]=product.p()
			  ks0d_eplus_eta[0]=product.momentum().eta()
			  ks0d_eplus_phi[0]=product.momentum().phi()
		  if product.particleID().pid()==-211:
			  ks0d_piminus_px[0]=product.momentum().x()
			  ks0d_piminus_py[0]=product.momentum().y()
			  ks0d_piminus_pz[0]=product.momentum().z()
			  ks0d_piminus_pT[0]=product.pt()
			  ks0d_piminus_p[0]=product.p()
			  ks0d_piminus_eta[0]=product.momentum().eta()
			  ks0d_piminus_phi[0]=product.momentum().phi()
		  if product.particleID().pid()==211:
			  ks0d_piplus_px[0]=product.momentum().x()
			  ks0d_piplus_py[0]=product.momentum().y()
			  ks0d_piplus_pz[0]=product.momentum().z()
			  ks0d_piplus_pT[0]=product.pt()
			  ks0d_piplus_p[0]=product.p()
			  ks0d_piplus_eta[0]=product.momentum().eta()
			  ks0d_piplus_phi[0]=product.momentum().phi()	
		    
	    t3.Fill()
	    # 	    #f3 = TFile('eraseme.root','recreate')
	    # 	    truthd_px[0]=product.momentum().x()
	    # 	    truthd_py[0]=product.momentum().y()
	    # 	    truthd_pz[0]=product.momentum().z()
	    # 	    truthd_pT[0]=product.pt()
	    # 	    truthd_p[0]=product.p()
	    # 	    truthd_eta[0]=product.momentum().eta()
	    # 	    truthd_phi[0]=product.momentum().phi()
	    # 	    truthd_pid[0]=product.particleID().pid()
	    # 	    truthd_evtid[0] = TES['Rec/Header'].evtNumber()
	    # 	    truthd_runid[0]= TES['Rec/Header'].runNumber()
	    # 	    t1.Fill()
	    # 	    ctruth+=1
	    # 	    if not ctruth%1000:
			    
	    # 		    t1.AutoSave()
		    
	    cks0t+=1
	    if not cks0t%100:
		    t3.AutoSave()
		    
	    
			    
	    	    
	    
    	    
    myprotos = filter(lambda x: get_mcpar(x)!=0,myprotos)
    myprotos = filter(lambda x: get_mcpar(x).mother(),myprotos)
    myprotos = filter(lambda x: any([get_mcpar(x).key() in lista for lista in products_keys_pipiee]),myprotos)
    for proto in myprotos:
	    
	    track = proto.track()
	    mcpar = get_mcpar(proto)
	    
	    mother = mcpar.mother()
	    
	    
	    
	    
           
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
	    if not creco%1000:
		    t4.AutoSave()



    
    
    
    proto_keys = map(lambda x: get_mcpar(x).key(),myprotos)
    
    for index in xrange(len(products_keys_pipiee)):
	    
	    if all(x in proto_keys for x in products_keys_pipiee[index]):
		    protos_temp = filter(lambda x: get_mcpar(x).key() in products_keys_pipiee[index],myprotos)
		    
		    for ks0proto in protos_temp:
			    ks0par = get_mcpar(ks0proto)
			    mother = ks0par.mother()
			    ks0track = ks0proto.track()
			    ks0_recod_evt_id[0]=TES['Rec/Header'].evtNumber()
			    ks0_recod_run_id[0]=TES['Rec/Header'].runNumber()

			    ks0_recod_px_truth[0]=mother.momentum().x()
			    ks0_recod_py_truth[0]=mother.momentum().y()
			    ks0_recod_pz_truth[0]=mother.momentum().z()
			   
			    ks0_recod_pT_truth[0]=mother.pt()
			    ks0_recod_p_truth[0]=mother.p()
			    ks0_recod_eta_truth[0] = mother.momentum().eta()
			    ks0_recod_phi_truth[0]=mother.momentum().phi()

			    ks0_recod_PV_x_truth[0]=mother.originVertex().position().x()
			    ks0_recod_PV_y_truth[0]=mother.originVertex().position().y()
			    ks0_recod_PV_z_truth[0]=mother.originVertex().position().z()
			    
			    ks0_recod_SV_x_truth[0]=mother.endVertices()[-1].position().x()
			    ks0_recod_SV_y_truth[0]=mother.endVertices()[-1].position().y()
			    ks0_recod_SV_z_truth[0]=mother.endVertices()[-1].position().z()
			    
			    if ks0par.particleID().pid()==11:
				    #f6 = TFile('eraseme.root','recreate')
				    ks0_recod_eminus_px[0]=ks0track.momentum().x()
				    ks0_recod_eminus_py[0]=ks0track.momentum().y()
				    ks0_recod_eminus_pz[0]=ks0track.momentum().z()
				    ks0_recod_eminus_p[0]=ks0track.p()
				    ks0_recod_eminus_pT[0]=ks0track.pt()
				    ks0_recod_eminus_eta[0]=ks0track.momentum().eta()
				    ks0_recod_eminus_phi[0]=ks0track.momentum().phi()
				    ks0_recod_eminus_trck_type[0]=ks0track.type()

			    if ks0par.particleID().pid()==-11:
				    
				    ks0_recod_eplus_px[0]=ks0track.momentum().x()
				    ks0_recod_eplus_py[0]=ks0track.momentum().y()
				    ks0_recod_eplus_pz[0]=ks0track.momentum().z()
				    ks0_recod_eplus_p[0]=ks0track.p()
				    ks0_recod_eplus_pT[0]=ks0track.pt()
				    ks0_recod_eplus_eta[0]=ks0track.momentum().eta()
				    ks0_recod_eplus_phi[0]=ks0track.momentum().phi()
				    ks0_recod_eplus_trck_type[0]=ks0track.type()
			    if ks0par.particleID().pid()==211:
				    
				    ks0_recod_piplus_px[0]=ks0track.momentum().x()
				    ks0_recod_piplus_py[0]=ks0track.momentum().y()
				    ks0_recod_piplus_pz[0]=ks0track.momentum().z()
				    ks0_recod_piplus_p[0]=ks0track.p()
				    ks0_recod_piplus_pT[0]=ks0track.pt()
				    ks0_recod_piplus_eta[0]=ks0track.momentum().eta()
				    ks0_recod_piplus_phi[0]=ks0track.momentum().phi()
				    ks0_recod_piplus_trck_type[0]=ks0track.type()


			    if ks0par.particleID().pid()==-211:
				    
				    ks0_recod_piminus_px[0]=ks0track.momentum().x()
				    ks0_recod_piminus_py[0]=ks0track.momentum().y()
				    ks0_recod_piminus_pz[0]=ks0track.momentum().z()
				    ks0_recod_piminus_p[0]=ks0track.p()
				    ks0_recod_piminus_pT[0]=ks0track.pt()
				    ks0_recod_piminus_eta[0]=ks0track.momentum().eta()
				    ks0_recod_piminus_phi[0]=ks0track.momentum().phi()
				    ks0_recod_piminus_trck_type[0]=ks0track.type()
	

	            
		    t2.Fill()
		    cks0r+=1
		    if not cks0r%1000:
		    	    t2.AutoSave()

f1.cd()	
#f1.WriteTObject(t1)
f1.WriteTObject(t2)
f1.WriteTObject(t3)
f1.WriteTObject(t4)
f1.Close()	

  


       





