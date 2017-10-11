# CONFIGURE DAVINCI (GENERAL CONFIGURATION OF THE JOB)



import ROOT
import numpy as np
import os
import sys
from SetGaudiTasks import * #xa importa gaudi e davinci e os.path


## SKIP EVENTS WITH NO TRACKS RECONSTRUCTED
## Vou a facer unha ntupla con todos os eventos

f1 = ROOT.TFile('/scratch13/acasais/MatchVeloLong/MathVeloLong.root','recreate') 
t1 = ROOT.TTree('aTree','aTree')


#inicializo os arrays
evt_id = np.zeros(1, dtype=int)
velo_eta = np.zeros(1, dtype=float)
velo_phi = np.zeros(1, dtype=float)
long_eta = np.zeros(1, dtype=float)
long_phi  = np.zeros(1, dtype=float)
delta_r  = np.zeros(1, dtype=float)
delta_z = np.zeros(1, dtype=float)
run_id = np.zeros(1,dtype=int)
 
t1.Branch('Event_no',evt_id,'Event_no/I')
t1.Branch('Run_no',run_id,'Run_no/I')
t1.Branch('Velo_eta',velo_eta,'Velo_eta/D')
t1.Branch('Velo_phi',velo_phi,'Velo_phi/D')
t1.Branch('Long_eta',long_eta,'Long_eta/D')
t1.Branch('Long_phi',long_phi,'long_phi/D')
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

'''
if int(sys.argv[1])>1: 
	gaudi.run(int(sys.argv[1])-1)
'''
unmxoatched_tracks = 0
for i in xrange(4):
	c1=gaudi.run(1)
        tracks = TES["Rec/Track/Best"]
       
	evt_id[0] = TES['Rec/Header'].evtNumber()
	run_id[0] = TES['Rec/Header'].runNumber()
   	
        if not tracks.size(): continue
        
	
	velo_tracks = []
	long_tracks = []
	for track in tracks:
	 	if not 'momentum' in dir(track): continue
		#print track.type
		if track.type() == 1: velo_tracks.append(track)
		if track.type() == 3: long_tracks.append(track)
	for track in velo_tracks:
		list_R = map(lambda x: [delR(track,x),x],long_tracks)
		list_R = filter(lambda x: x[0]<0.2,list_R)
	if len(list_R)>0: break
		
				
		
				

			
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

