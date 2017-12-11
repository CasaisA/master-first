from ROOT import *
import numpy as np


f = TFile('/scratch13/acasais/TrackMatching/TrackMatching1-30000.root')
t = f.Get('aTree')

#vou a quitar aqueles eventos q estean na tupla de MatchVeloLong          
f2 = TFile('/scratch13/acasais/MatchVeloLong/MatchVeloLong1-40000.root')
t2 = f2.Get('aTree')
fera2 = TFile('eraseme2.root','RECREATE')
hP=TH1F('p wo ghosts','',300,0,20000)
heta = TH1F('eta wo ghosts','',500,0,8)
hphi = TH1F('phi wo ghosts','',20,-np.pi,np.pi)

# esto vai moi lento                                                      
event_no = 0
events=[]
#usar copytree!                                                           

for evt in t:
    if event_no != evt.Event_no:
        events.append(evt.Event_no)
        event_no = evt.Event_no
t3 = t.CopyTree('Track_type==1')
event_no = 0

matches = 0 
for evt in events:
    if event_no != evt:
        
        
        fera = TFile('eraseme.root','RECREATE')
        event_no = evt
        tevent = t3.CopyTree('Event_no=='+str(event_no))
        t2event = t2.CopyTree('Event_no=='+str(event_no))
        if t2event.GetEntries()==0 or tevent.GetEntries==0: continue
        for ev1 in tevent:
                flag = 0
                for ev2 in t2event:
                    if (ev1.Track_px == ev2.Long_px and ev1.Track_py == ev2.Long_py and ev1.Track_pz == ev2.Long_pz) or (ev1.Track_px == ev2.Velo_px and ev1.Track_py == ev2.Velo_py and ev1.Track_pz == ev2.Velo_pz):
                        matches +=1
                        flag = 1
                        if matches % 1000 == 0: print matches
                        break
                    
                if flag == 0: 
			hP.Fill(ev1.Particle_P)
                        heta.Fill(ev1.Particle_eta)
			hphi.Fill(ev1.Particle_phi)  
f.Close()
f2.Close()


fhist =TFile('HwoGhosts-notree.root','recreate')
fhist.cd()
hP.Write('P wo ghosts')
heta.Write('eta wo ghosts')
hphi.Write('phi wo ghosts')
fhist.Close()

