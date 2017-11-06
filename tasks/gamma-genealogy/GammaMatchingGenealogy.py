#! /usr/:bin/env python
# CONFIGURE DAVINCI (GENERAL CONFIGURATION OF THE JOB)
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
	





if int(sys.argv[1])>1: 
	gaudi.run(int(sys.argv[1])-1)
unmatched_tracks = 0
frame_total=pd.DataFrame()
ind=-1
for i in range(int(sys.argv[2])-int(sys.argv[1])+1):
	vars = {}
	c1=gaudi.run(5)
        tracks = TES["Rec/Track/Best"]
        particles = TES["MC/Particles"]
	photons = filter(lambda x: particlePID(x)==22,particles)
	vars['evt_id'] = TES['Rec/Header'].evtNumber()
	vars['run_id'] = TES['Rec/Header'].runNumber()
   	#if not particles: break  ## <--- use this condition to know when the dst is finished
        #if not tracks.size(): continue
        
	
	
	for track in tracks:
	 	if not 'momentum' in dir(track): continue
	
		
		
		list_R = map(lambda x: [delR(track,x),x],photons)
		list_Z = map(lambda x: [delZ(track,x),x],photons)
		list_R = filter(lambda x: x[0]<0.1,list_R)
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
		vars['delta_r'] = myParticle[0][0]
		vars['delta_z'] = myParticle[0][1]
				

			
		#o run id e evt id xa esta cuberto	
		vars['trck_eta']=track.momentum().eta()
		vars['trck_phi']=track.momentum().phi()
		trck_px=track.momentum().x(); vars['trck_px']=trck_px
		trck_py=track.momentum().y(); vars['trck_py']=trck_py
		trck_pz=track.momentum().z(); vars['trck_pz']=trck_pz
		vars['trck_pT']=np.sqrt(trck_px**2+trck_py**2)
		vars['trck_P']=np.sqrt(trck_px**2+trck_py**2+trck_pz**2)
		vars['trck_type']=track.type()
		vars['part_eta']=particle.momentum().eta()
		vars['part_phi']=particle.momentum().phi()
		part_px=particle.momentum().x();vars['part_px']=part_px
		part_py=particle.momentum().y();vars['part_py']=part_py
		part_pz=particle.momentum().z(); vars['part_pz']=part_pz
		vars['part_pT']=np.sqrt(part_px**2+part_py**2)
		vars['part_P']=np.sqrt(part_px**2+part_py**2+part_pz**2)		


		vars['part_pid']=particle.particleID().pid()
		#delta_r[0] = dr
		#delta_z[0] = dz
		mothers = []
		vars['list_mothers'] = [findMothers(particle,mothers)]
		vars['list_vertices'] = [findVertices(particle)]
		
		vars['delR_mother']= delR(track,particle.mother())
		vars['delZ_mother'] = delZ(track,particle.mother())
		ind+=1
		frame_temp = pd.DataFrame(data=vars,index=[ind])
		frame_total=frame_total.append(frame_temp)
gaudi.stop(); gaudi.finalize() 
contador=0
for i in frame_total.get('list_mothers'):
	if abs(i[0])==11: contador+=1
print float(contador)/len(frame_total.get('list_mothers'))

lista_nais=frame_total['list_mothers'].values.tolist()
nais = []
for nai in lista_nais:
	nais.append(nai[0])
with open('nais.txt', 'wb') as f:
    pickle.dump(nais, f)

hist = plt.hist(nais,bins=600,range=[-300,300])
plt.xlabel('ID da nai')
plt.ylabel('No. Entries')

# f1.cd()
# t1.Write()
# f1.Close()
# if len(sys.argv):
# 	f = ROOT.TFile('/scratch13/acasais/track_matching'+str(sys.argv[1])+'-'+str(sys.argv[2])+'.root')
	


				
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


