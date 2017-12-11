#! /usr/bin/env python

## CONFIGURE DAVINCI (GENERAL CONFIGURATION OF THE JOB)
from Configurables import DaVinci, ChargedPP2MC, ChargedProtoParticleMaker
import GaudiPython
from Gaudi.Configuration import *
import pandas as pd
import math as m 
DaVinci().EvtMax = 0
DaVinci().DataType = "2012"
DaVinci().Simulation = True
## These are for data tags (magnet up or down?)
DaVinci().DDDBtag  = "dddb-20130929-1"
DaVinci().CondDBtag = "sim-20130522-1-vc-mu100"
magnet = 'up'
## INPUT DSTS, POTENTIALLY ADD MORE
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

#DaVinci().Input = ['PFN:root://eoslhcb.cern.ch//eos/lhcb/grid/prod/lhcb/MC/2012/ALLSTREAMS.DST/00037694/0000/00037694_00000001_1.allstreams.dst']

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


    

electrons = pd.DataFrame()
num_v_e=0
num_l_e=0
den_e=0
	
num_v_pi=0
num_l_pi=0
den_pi=0
for i in range(1000):
	vars = {}
	c1=gaudi.run(1)
	tracks = TES["Rec/Track/Best"]
	

	mcparticles = TES["MC/Particles"]
	#photons = filter(lambda x: particlePID(x)==22,particles)
	vars['evt_id'] = TES['Rec/Header'].evtNumber()
	vars['run_id'] = TES['Rec/Header'].runNumber()
	#if not mcparticles.size(): break
	if not tracks.size(): continue

	## GET FULL LIST OF PROTO PARTICLES: ONE PER TRACK IN REC/TRACK/BEST
	myprotos = TES["Rec/ProtoP/MyProtoParticles"]
	## ERASES THE CASES WHERE 'NOT OK' IN THE get_mcpar(x) FUNCTION
	myprotos= filter(lambda x: get_mcpar(x)!=0,myprotos)
        ## I ONLY TAKE VELO TRACKS
	myprotos_velo = filter(lambda x: x.track().type()==1,myprotos)
	myprotos_long = filter(lambda x: x.track().type()==3,myprotos)
	
	##FILTERS ONLY THE ELECTRONS
	myprotos_velo_e = filter(lambda x: abs(get_mcpar(x).particleID().pid())==11,myprotos_velo)
	myprotos_long_e = filter(lambda x: abs(get_mcpar(x).particleID().pid())==11,myprotos_long)
	myprotos_velo_pi= filter(lambda x: abs(get_mcpar(x).particleID().pid())==211,myprotos_velo)
	myprotos_long_pi= filter(lambda x: abs(get_mcpar(x).particleID().pid())==211,myprotos_long)

        #FOR THE NUMERATOR IN THE EFFICIENCY
	myelectrons = filter(lambda x: abs(x.particleID().pid())==11,mcparticles)
	mypions= filter(lambda x: abs(x.particleID().pid())==211,mcparticles)
	
	num_v_e+=len(myprotos_velo_e)
	num_l_e+=len(myprotos_long_e)
	den_e+=len(myelectrons)
	
	num_v_pi+=len(myprotos_velo_pi)
	num_l_pi+=len(myprotos_long_pi)
	den_pi+=len(mypions)
	
eficiencia_v_e = float(num_v_e)/den_e
eficiencia_l_e = float(num_l_e)/den_e

eficiencia_v_pi = float(num_v_pi)/den_pi
eficiencia_l_pi = float(num_l_pi)/den_pi

print 'Velo electrons eficiency = ',eficiencia_v_e
print 'Long electrons eficiency = ',eficiencia_l_e
print 'Velo pions eficiency = ',eficiencia_v_pi
print 'Long pions eficiency = ',eficiencia_l_pi
	




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
