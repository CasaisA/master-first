#! /usr/:bin/env python
# CONFIGURE DAVINCI (GENERAL CONFIGURATION OF THE JOB)
from Configurables import DaVinci
import GaudiPython
import os.path
import ROOT
import numpy as np
#vou facer o root file onde meter todo e vou fixar as branches






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

 
f = ROOT.TFile('variables.root','recreate')
t1 = ROOT.TTree('aTree','aTree')


#inicializo os arrays
evt_id = np.zeros(1, dtype=float)
trck_eta = np.zeros(1, dtype=float)
trck_phi = np.zeros(1, dtype=float)
trck_type = np.zeros(1, dtype=float)
part_eta = np.zeros(1, dtype=float)
part_pid = np.zeros(1, dtype=float)
part_phi  = np.zeros(1, dtype=float)
delta_r  = np.zeros(1, dtype=float)

t1.Branch('Event_id',evt_id,'Event_id/D')
t1.Branch('track_eta',trck_eta,'track_eta/D')
t1.Branch('track_phi',trck_phi,'track_phi/D')
t1.Branch('track_type',trck_type,'track_type/D')
t1.Branch('partitlce_eta',part_eta,'particle_eta/D')
t1.Branch('particle_phi',part_phi,'particle_phi/D')
t1.Branch('particle_pid',part_pid,'particle_pid/D')
t1.Branch('detal_r',delta_r,'detal_r/D')

#arrancamos gaudi
TES = gaudi.evtsvc()

tracks_dict = {}
particles_dict = {}
def delPhi(x,y):
	if np.abs(x-y)<=np.pi:
		return np.abs(x-y)
	else:
		return np.abs(2*np.pi-np.abs(x-y))

event_id= 1
unmatched_tracks = 0
for i in range(2):
	event_id += 1
	c1=gaudi.run(1)
        tracks = TES["Rec/Track/Best"]
        particles = TES["MC/Particles"]
   	if not particles: break  ## <--- use this condition to know when the dst is finished
        if not tracks.size(): continue
        if not particles.size(): continue
	dphi = []
	deta = []
	dr =[]
	trck_no=0
	trck_wo_p=0
	for j in xrange(tracks.size()):
	#	if not particles[j].momentum(): continue
	 	if not 'momentum' in dir(tracks[j]):
			trck_wo_p += 1	
			continue
		
		dphi = []
		deta = []
		dr = []
		
		part_wo_p=0
		for k in xrange(particles.size()):
			
			if  'momentum' in dir(particles[k]):
				dphi.append(delPhi(tracks[j].momentum().phi(),particles[k].momentum().phi()))
				deta.append(tracks[j].momentum().eta()-particles[k].momentum().eta())		
				dr.append(np.sqrt(deta[k]**2+dphi[k]**2))
				
			else: 
				deta.append(1000)
				dphi.append(1000)
				dr.append(1000)	
		
		if min(dr)<.5:
			evt_id[0]=event_id
			trck_eta[0]=tracks[j].momentum().eta()
			trck_phi[0]=tracks[j].momentum().phi()
			trck_type[0]=tracks[j].type()
			part_eta[0]=particles[dr.index(min(dr))].momentum().eta()
			part_phi[0]=particles[dr.index(min(dr))].momentum().eta()
			part_pid[0]=particles[dr.index(min(dr))].momentum().eta()
			delta_r[0] = dr[dr.index(min(dr))]
			t1.Fill()
		else: unmatched_tracks += 1

f = ROOT.TFile('variables.root','recreate')
#t1.Write(); f.Close()				
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

