#! /usr/bin/env python

## CONFIGURE DAVINCI (GENERAL CONFIGURATION OF THE JOB)
from Configurables import DaVinci, ChargedPP2MC, ChargedProtoParticleMaker
import GaudiPython
from Gaudi.Configuration import *

DaVinci().EvtMax = 0
DaVinci().DataType = "2012"
DaVinci().Simulation = True
## These are for data tags (magnet up or down?)
DaVinci().DDDBtag  = "dddb-20130929-1"
DaVinci().CondDBtag = "sim-20130522-1-vc-mu100"

## INPUT DSTS, POTENTIALLY ADD MORE
magnet = 'up'
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

for i in range(5):
    c1=gaudi.run(1)
    tracks = TES["Rec/Track/Best"]
    mcparticles = TES["MC/Particles"]
    #if not mcparticles.size(): break
   # if not tracks.size(): continue

    ## GET FULL LIST OF PROTO PARTICLES: ONE PER TRACK IN REC/TRACK/BEST
    myprotos = TES["Rec/ProtoP/MyProtoParticles"]
    ## EXAMPLE, GET PROTO TRACKS CORRESPONDING TO VELO TRACKS
    myprotos = filter(lambda x: x.track().type()==1,myprotos)
    ## AND NOW, MC PARTICLE MATCHED
    cbreak = 0
    for myproto in myprotos:
        mcpar = get_mcpar(myproto)
        ## FOUND AN ELECTRON FROM KS0!
        if mcpar and abs(mcpar.particleID().pid())==11 and mcpar.mother() and abs(mcpar.mother().particleID().pid())==310: cbreak=1;break
    if cbreak: break

## PRINT SOME INFO, IF CANDIDATE FOUND
if i<99:
    ks0 = mcpar.mother()
    print map(lambda x: x.particleID().pid(),ks0.endVertices()[0].products())
    tr = myproto.track()
    print mcpar.momentum().eta(),mcpar.momentum().phi(),tr.momentum().eta(),tr.momentum().phi()


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
