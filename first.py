#! /usr/:bin/env python
# CONFIGURE DAVINCI (GENERAL CONFIGURATION OF THE JOB)
from Configurables import DaVinci
import GaudiPython
import os.path

DaVinci().EvtMax = 0
DaVinci().DataType = "2012"
DaVinci().Simulation = True
## These are for data tags (magnet up or down?)
DaVinci().DDDBtag  = "dddb-20130929-1"
DaVinci().CondDBtag = "sim-20130522-1-vc-md100"

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

gaudi = GaudiPython.AppMgr()
gaudi.initialize()

## SKIP EVENTS WITH NO TRACKS RECONSTRUCTED
## Vou a facer unha ntupla con todos os eventos 
TES = gaudi.evtsvc()
'''
f = ROOT.TFile('variables.root','recreate')
t = ROOT.TTree('aTree','aTree')

pETA = np.zeros(1, dtype=float)
pPHI = np.zeros(1, dtype=float)
pPID = np.zeros(1, dtype=float)
tETA = np.zeros(1, dtype=float)
tPHI = np.zeros(1, dtype=float)
tTYPE = np.zeros(1, dtype=float)

t.Branch('pETA',pETA,'pETA/D')
t.Branch('pPHI',pPHI,'pPHI/D')
t.Branch('pPID',pPID,'pPID/D')
t.Branch('tETA',tETA,'tETA/D')
t.Branch('tPHI',tPHI,'tPHI/D')
t.Branch('tTYPE',tTYPE,'tTYPE/D')

'''


for i in range(100):
    c1=gaudi.run(1)
    tracks = TES["Rec/Track/Best"]
    mcparticles = TES["MC/Particles"]
    if not mcparticles: break
 ## <--- use this condition to know when the dst is finished
    if not tracks.size(): continue
    if not mcparticles.size(): continue
    if not mcparticles.size(): continue
    tracks_dict={}
    particles_dict={}
    tracks_dict['eta']=[]
    tracks_dict['phi']=[]
    tracks_dict['type']=[]
    particles_dict['eta']=[]
    particles_dict['phi']=[]
    particles_dict['pid']=[]
    for j in xrange(tracks.size()):
	    
	    if not tracks[j]: continue
	    tracks_dict['eta'][0]=tracks[j].momentum().eta()
	    tracks_dict['phi'][0]=tracks[j].momentum().phi()
	    tracks_dict['type'][0]=tracks[j].type()
	   
 for j in xrange(mcparticles.size()):
	    if not mcparticles[j]: continue
	    
	    particles_dict['eta'][0]=mcparticles[j].momentum().eta()
	    particles_dict['phi'][0]=mcparticles[j].momentum().phi()
	    particles_dict['pid'][0]=mcparticles[j].momentum().phi()    
	    
   
'''
esta e unha forma de ver cousas que hai na DST 
particle = mcparticles[0]
# could also be
# for particle in mcparticles: ...
print particle.momentum().eta()
print particle.momentum().phi()
print particle.particleID().pid()
if particle.mother(): print particle.mother().particleID().pid()

if tracks.size(): track = tracks[0]
print track.momentum().eta()
print track.momentum().phi()
print track.type()
'''
#// -----------------
#// track typology:
#//-----------------
#// trtype = 1 Velo
#// trtype = 2 VeloR
#// trtype = 3 Long
#// trtype = 4 Upstream
#// trtype = 5 Downstream
#// trtype = 6 Ttrack
#// trtype = 7 Muon

# lb-run DaVinci/v42r5p1 tcsh -f
# emacs file

# define DeltaR = sqrt(Delta_Phi**2 + Delta_Eta**2)
# when you define Delta_Phi, bear in mind that Delta_Phi b/t 10 degrees and 350 degrees is 20, not 340!

# both: try to write ntuples with all the information. Use the code in my presentation
# both: add more dsts in the same folder
# both: use screen to leave jobs running in background

# Alexandre. Study downstream tracks.
#  - Fraction of downstream tracks with respect to all tracks
#  - Match downstream tracks to long tracks. Fraction of times you get a deltap/p below 5%? Fraction of times you get a DeltaR< 0.25?
#  - Match downstream tracks to mcparticles. Use smallest deltap and smallest delta R. Is the result always the same?
#  - Distribution of the IDs of the mcparticles matched to downstream tracks. Also, distribution of their mothers.


# Adrian. Study velo (upstream) tracks.
#  - Fraction of VELO tracks with respect to all tracks
#  - Match velo tracks to long tracks. Fraction of times you get a DeltaR< 0.25?
#  - Match velo tracks to mcparticles. Use smallest delta R.
#  - Distribution of the IDs of the mcparticles matched to VELO tracks.
#  - Momentum distribution of the mcparticles matched to VELO tracks. Same with eta and phi. Compare cases when close long tracks are present or not.

