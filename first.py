#! /usr/:bin/env python
# CONFIGURE DAVINCI (GENERAL CONFIGURATION OF THE JOB)
from Configurables import DaVinci
import GaudiPython
import os.path
import ROOT
import numpy as np
import os
import sys

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

f1 = ROOT.TFile('/scratch13/acasais/track_matching'+str(sys.argv[1])+'-'+str(sys.argv[2])+'.root','recreate') 
t1 = ROOT.TTree('aTree','aTree')


#inicializo os arrays
evt_id = np.zeros(1, dtype=int)
trck_eta = np.zeros(1, dtype=float)
trck_phi = np.zeros(1, dtype=float)
trck_type = np.zeros(1, dtype=int)
part_eta = np.zeros(1, dtype=float)
part_pid = np.zeros(1, dtype=int)
part_moth_pid = np.zeros(1, dtype=int)
part_phi  = np.zeros(1, dtype=float)
delta_r  = np.zeros(1, dtype=float)
delta_z = np.zeros(1, dtype=float)
run_id = np.zeros(1,dtype=int)
 
t1.Branch('Event_no',evt_id,'Event_no/I')
t1.Branch('Run_no',run_id,'Run_no/I')
t1.Branch('Track_eta',trck_eta,'Track_eta/D')
t1.Branch('Track_phi',trck_phi,'Track_phi/D')
t1.Branch('Track_type',trck_type,'Track_type/I')
t1.Branch('Partitlce_eta',part_eta,'Particle_eta/D')
t1.Branch('Particle_phi',part_phi,'Particle_phi/D')
t1.Branch('Particle_pid',part_pid,'Particle_pid/I')
t1.Branch('Mother_pid',part_moth_pid,'Particle_mother_pid/I')
t1.Branch('Delta_r',delta_r,'Delta_r/D')
t1.Branch('Delta_z',delta_z,'Delta_z/D')

TES = gaudi.evtsvc()

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


if int(sys.argv[1])>1: 
	gaudi.run(int(sys.argv[1])-1)
unmatched_tracks = 0
for i in range(int(sys.argv[2])-int(sys.argv[1])+1):
	c1=gaudi.run(1)
        tracks = TES["Rec/Track/Best"]
        particles = TES["MC/Particles"]
	evt_id[0] = TES['Rec/Header'].evtNumber()
	run_id[0] = TES['Rec/Header'].runNumber()
   	if not particles: break  ## <--- use this condition to know when the dst is finished
        if not tracks.size(): continue
        if not particles.size(): continue
	
	
	for track in tracks:
	 	if not 'momentum' in dir(track): continue
	
		
		
		list_R = map(lambda x: [delR(track,x),x],particles)
		list_Z = map(lambda x: [delZ(track,x),x],particles)
		list_R = filter(lambda x: x[0]<0.5,list_R)
		list_Z = filter(lambda x: x[0]<100,list_Z)		
					
			
		list_R.sort(); list_Z.sort()
		myParticle = []
		
		for R in list_R:
			for Z in list_Z:
				if R[1] == Z[1]:
					myParticle.append([R[0],Z[0],R[1]])
					break
		if len(myParticle)>0:
			myParticle.sort()
		if len(myParticle)==0:
			unmatched_tracks+=1 
			continue
		particle = myParticle[0][2]
		delta_r[0] = myParticle[0][0]
		delta_z[0] = myParticle[0][1]
				

			
		#o run id e evt id xa esta cuberto	
		trck_eta[0]=track.momentum().eta()
		trck_phi[0]=track.momentum().phi()
		trck_type[0]=track.type()
		part_eta[0]=particle.momentum().eta()
		part_phi[0]=particle.momentum().phi()
		part_pid[0]=particle.particleID().pid()
		#delta_r[0] = dr
		#delta_z[0] = dz
		if particle.mother():
			part_moth_pid[0]=particle.mother().particleID().pid()
		else: part_moth_pid[0]=0
		t1.Fill()
gaudi.stop(); gaudi.finalize() 


f1.cd()
t1.Write()
f1.Close()
if len(sys.argv):
	f = ROOT.TFile('/scratch13/acasais/track_matching'+str(sys.argv[1])+'-'+str(sys.argv[2])+'.root')
	


				
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

