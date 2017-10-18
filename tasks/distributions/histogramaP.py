from ROOT import *
import numpy as np


f = TFile('/scratch13/acasais/TrackMatching/TrackMatching1-30000.root')
t = f.Get('aTree')

#vou a quitar aqueles eventos q estean na tupla de MatchVeloLong          
f2 = TFile('/scratch13/acasais/MatchVeloLong/MatchVeloLong1-40000.root') t2 = f2.Get('aTree')
hP2=TH1F('P w/o ghosts','',500,0,20000)
fhist =TFile('Histograma.root','recreate')
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


for evt in events:
    if event_no != evt:
        fera = TFile('eraseme.root','RECREATE')
        event_no = evt
        tevent = t3.CopyTree('Event_no=='+str(event_no))
        t2event = t2.CopyTree('Event_no=='+str(event_no))
        if t2event.GetEntries()==0 or tevent.GetEntries==0: continue
        for ev1 in tevent:
                for ev2 in t2event:
                    if (ev1.Track_px == ev2.Long_px and ev1.Track_py == ev2.Long_py) or (ev1.Track_px == ev2.Velo_px and ev1.Track_py == ev2.Velo_px):


                        continue
                    else:
			hP2.Fill(ev1.Particle_P)                          
                                                                          
fhist.cd()
hP2.Write('P w/o ghosts')
fhist.Close()

