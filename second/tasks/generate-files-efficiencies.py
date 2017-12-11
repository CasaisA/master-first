#! /usr/bin/env python

## CONFIGURE DAVINCI (GENERAL CONFIGURATION OF THE JOB)
from Configurables import DaVinci, ChargedPP2MC, ChargedProtoParticleMaker
import GaudiPython
from Gaudi.Configuration import *
import pandas as pd
import math as m
import pickle
import os
DaVinci().EvtMax = 0
DaVinci().DataType = "2012"
DaVinci().Simulation = True
## These are for data tags (magnet up or down?)
DaVinci().DDDBtag  = "dddb-20130929-1"
DaVinci().CondDBtag = "sim-20130522-1-vc-mu100"

## INPUT DSTS, POTENTIALLY ADD MORE
magnet='up'
dst_file = []
for i in xrange(1,71):
        i = str(i)
        if int(i)<10:
                dst_file_name = '/scratch29/KsPiPiee/'+magnet+'00037694_0000000'+i+'_1.allstreams.dst'
        else:
                dst_file_name = '/scratch29/KsPiPiee/'+magnet+'/00037694_000000'+i+'_1.allstreams.dst'

        if os.path.isfile(dst_file_name):
                dst_file.append(dst_file_name)

DaVinci().Input = dst_file

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

mctruth = pd.DataFrame()
reco = pd.DataFrame()


indtruth = -1##index for the data frame
indreco = -1
#RANGE IS AS BIG AS YOU WANT IT TO BE
for i in range(100000):
    c1 = gaudi.run(1)
    truthd={}
    recod={}
    tracks = TES["Rec/Track/Best"]
    mcparticles = TES["MC/Particles"]
    myprotos = TES["Rec/ProtoP/MyProtoParticles"]
    truthd['evt_id'] = TES['Rec/Header'].evtNumber()
    recod['evt_id']=truthd['evt_id']
    truthd['run_id'] = TES['Rec/Header'].runNumber()
    recod['run_id']=truthd['run_id']
    
    for particle in mcparticles:
	    mother = particle.mother()
	    if not mother: continue
	    end_vertices =map(lambda x: x.particleID().pid(),mother.endVertices()[0].products())
	    ks0= False
	    #print end_vertices
	    if 211 in end_vertices and -211 in end_vertices and 11 in end_vertices and -11 in end_vertices:
		    ks0 = True
	    if ks0:
		    truthd['px']=particle.momentum().x()
		    truthd['py']=particle.momentum().y()
		    truthd['pz']=particle.momentum().z()
		    truthd['pT']=m.sqrt(truthd['px']**2+truthd['py']**2)
		    truthd['p']=m.sqrt(truthd['px']**2+truthd['py']**2+truthd['pz']**2)
		    truthd['eta']=particle.momentum().eta()
		    truthd['phi']=particle.momentum().phi()
		    truthd['pid']=particle.particleID().pid()
		    indtruth+=1
		    temp_truth = pd.DataFrame(data=truthd,index=[indtruth])
		    mctruth = mctruth.append(temp_truth)
    for proto in myprotos:
	    track = proto.track()
	    mcpar = get_mcpar(proto)
	    if mcpar == 0: continue
	    mother = mcpar.mother()
	    if not mother: continue
	    end_vertices =\
	              map(lambda x: x.particleID().pid(),\
			   mother.endVertices()[0].products())
	    
	    ks0= False
	    #print end_vertices
	    if 211 in end_vertices and -211 in end_vertices and 11 in\
	       end_vertices and -11 in end_vertices:
		    ks0 = True
	    if ks0:
		    recod['px']=track.momentum().x()
		    recod['py']=track.momentum().y()
		    recod['pz']=track.momentum().z()
		    recod['pT']=m.sqrt(recod['px']**2+recod['py']**2)
		    recod['p']=m.sqrt(recod['px']**2+\
				      recod['py']**2+recod['pz']**2)
		    recod['px_truth']=mcpar.momentum().x()
		    recod['py_truth']=mcpar.momentum().y()
		    recod['pz_truth']=mcpar.momentum().z()
		    recod['pT_truth']=m.sqrt(recod['px_truth']**2+recod['py_truth']**2)
		    recod['p_truth']=m.sqrt(recod['px_truth']**2+\
				      recod['py_truth']**2+recod['pz_truth']**2)
		    recod['eta']=track.momentum().eta()
		    recod['phi']=track.momentum().phi()
		    recod['eta_truth']=mcpar.momentum().eta()
		    recod['phi_truth']=mcpar.momentum().phi()
		    recod['pid']=mcpar.particleID().pid()
		    recod['trck_type']=track.type()
		    recod['mother_key']=mcpar.mother().key()
		    indreco+=1
    
		    temp_reco = pd.DataFrame(data=recod,index=[indreco])
		    reco = reco.append(temp_reco)

            
	

	
with open('/scratch13/acasais/second/task1/truth-500runs.p', 'wb') as f:
    pickle.dump(mctruth, f)

with open('/scratch13/acasais/second/task1/reco-500runs.p', 'wb') as p:
    pickle.dump(reco, p)



       





