#! /usr/bin/env python

## CONFIGURE DAVINCI (GENERAL CONFIGURATION OF THE JOB)
from Configurables import DaVinci, ChargedPP2MC, ChargedProtoParticleMaker
import GaudiPython
from Gaudi.Configuration import *
from Configurables import DaVinci
import GaudiPython
import os.path
import ROOT
import numpy as np
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import pickle

DaVinci().EvtMax = 0
DaVinci().DataType = "2012"
DaVinci().Simulation = True
## These are for data tags (magnet up or down?)
DaVinci().DDDBtag  = "dddb-20130929-1"
DaVinci().CondDBtag = "sim-20130522-1-vc-mu100"


## INPUT DSTS, POTENTIALLY ADD MORE (estan todas incorporadas agora)
dst_file = []
for i in xrange(1,34):
	i = str(i)
	if int(i)<10: 
		dst_file_name = '/scratch13/MC2012MB/00040748_0000000'+i+'_2.AllStreams.dst'
	else: 
		dst_file_name = '/scratch13/MC2012MB/00040748_000000'+i+'_2.AllStreams.dst'
	
	if os.path.isfile(dst_file_name):
		dst_file.append(dst_file_name)
DaVinci().Input = dst_file

#FUNCIONS DE INTERESE
def delPhi(x,y):
	if np.abs(x-y)<=np.pi:
		return np.abs(x-y)
	else:
		return np.abs(2*np.pi-np.abs(x-y))

def delR(track,particle):
	dphi = delPhi(track.momentum().phi(),particle.momentum().phi())
        deta = track.momentum().eta()-particle.momentum().eta()
        return np.sqrt(deta**2+dphi**2)
def delZ(track,particle):
	return np.abs(track.position().z()- particle.originVertex().position().z())

def particlePID(particle):
	        return particle.particleID().pid()



#funcion recursiva para atopar nais
def findMothers(particle,mothers):
	if particle.mother():
		mothers.append(particle.mother().particleID().pid())
		return findMothers(particle.mother(),mothers)
		
	else:
		return mothers

def findVertices(particle):
	vertices= []
	if len(particle.endVertices())>0:
		for product in particle.endVertices()[0].products():
			vertices.append(product.particleID().pid())
	else: vertices = []	
	return vertices





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




frame_total=pd.DataFrame()
ind=-1
for i in range(1000):
    
    vars = {}
    c1=gaudi.run(1)
    tracks = TES["Rec/Track/Best"]
    pv = TES["Rec/Vertex/Primary"][0]
    pv.tracks()
    mcparticles = TES["MC/Particles"]
    #photons = filter(lambda x: particlePID(x)==22,particles)
    vars['evt_id'] = TES['Rec/Header'].evtNumber()
    vars['run_id'] = TES['Rec/Header'].runNumber()
    if not mcparticles.size(): break
    if not tracks.size(): continue

    ## GET FULL LIST OF PROTO PARTICLES: ONE PER TRACK IN REC/TRACK/BEST
    myprotos = TES["Rec/ProtoP/MyProtoParticles"]
    ## EXAMPLE, GET PROTO TRACKS CORRESPONDING TO VELO TRACKS
    myprotos = filter(lambda x: x.track().type()==1,myprotos)
    ## ERASES THE CASES WHERE 'NOT OK' IN THE get_mcpar(x) FUNCTION
    myprotos= filter(lambda x: get_mcpar(x)!=0,myprotos)
    #myphotons= filter(lambda x: get_mcpar(x).particleID().pid()==22,myprotos)
    ## AND NOW, MC PARTICLE MATCHED
    cbreak = 0
    for proto in myprotos:
       particle = get_mcpar(proto)
       track = proto.track()
       
       vars['trck_eta']=abs(track.momentum().eta())
       vars['trck_phi']=track.momentum().phi()
       trck_px=track.momentum().x(); vars['trck_px']=trck_px
       trck_py=track.momentum().y(); vars['trck_py']=trck_py
       trck_pz=track.momentum().z(); vars['trck_pz']=trck_pz
       vars['trck_pT']=np.sqrt(trck_px**2+trck_py**2)
       vars['trck_P']=np.sqrt(trck_px**2+trck_py**2+trck_pz**2)
       vars['trck_type']=track.type()
       vars['part_eta']=abs(particle.momentum().eta())
       vars['part_phi']=particle.momentum().phi()
       part_px=particle.momentum().x();vars['part_px']=part_px
       part_py=particle.momentum().y();vars['part_py']=part_py
       part_pz=particle.momentum().z(); vars['part_pz']=part_pz
       vars['part_pT']=np.sqrt(part_px**2+part_py**2)
       vars['part_P']=np.sqrt(part_px**2+part_py**2+part_pz**2)
       vars['part_pid']=particle.particleID().pid()              
       vars['delR']=delR(track,particle)
       vars['delZ']=delZ(track,particle)
       ind+=1
       frame_temp = pd.DataFrame(data=vars,index=[ind])
       frame_total=frame_total.append(frame_temp)


with open('matching_bo.p', 'wb') as f:
    pickle.dump(frame_total, f)

## PRINT SOME INFO, IF CANDIDATE FOUND
# if i<99:
#     ks0 = mcpar.mother()
#     print map(lambda x: x.particleID().pid(),ks0.endVertices()[0].products())
#     tr = myproto.track()
#     print mcpar.momentum().eta(),mcpar.momentum().phi(),tr.momentum().eta(),tr.momentum().phi()


## TASKS
## ALEXANDRE. USE MINBIAS SAMPLE.
## Select Ks->pipi in long-long or downstream-downstream modes
## Determine reconstruction efficiency in both cases. For this, for the denominator take Kspipi MCTruth decaying with z<800 (for long-long) and 800<z<1000 (for downstream-dowstream)
## Compare momentum resolution for long and downstream tracks in both cases
## Compare mass resolution in both cases
## Compare DOCA, KsIP, KsLifeTime, pions IP, pions pT, pions eta in both cases

## ADRIAN. USE KS->pipiee sample
## Compare the reconstruction efficiency of long-track pions from the Ks->pipiee, velo-track pions from the Ks->pipiee and the same for electrons. Just do it track by track. Do the total and also as a function of the pion/electron momentum.
## Also, select Ks->pipiee using 4 long tracks or using 3 long tracks and 1 velo tracks. Or two long tracks and two velo tracks. Look at the efficiency ratio of these. You can use the total number of events in the denominator.
## For Ks->pipiee, use the kinematical constraint from the SV and PV position to determine the Ks mass. For 4 long, use the standard mass. Alternatively, for 4 long, ignore the smallest electron momentum. For 3 long + velo, ignore the velo track momentum. For 2 long + 2 velo, assume the 2 velo tracks have the same momentum and use that in the equations.
## For Ks->pipiee, look at cases in which you have two long track pions and one long track electron, and nothing else. Efficiency for that?
