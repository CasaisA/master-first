# -*- coding: utf-8 -*-
from ROOT import *
import numpy as np

f = TFile('/scratch13/acasais/TrackMatching/TrackMatching1-30000.root')
t = f.Get('aTree')

#Fraction of Velo Tracks
ratio = float(t.GetEntries('Track_type==1'))/t.GetEntries()
#Distribution of the IDs of the mcparticles amtched to VELO tracks

h = TH1F('ID','',600,-300,300)
t.Project('ID','Particle_pid','Track_type == 1')
##
c = TCanvas()
h.Draw()
for i in xrange(1,600):
    bincont = h.GetBinContent(i)
    if bincont>0:
        print 'MCid= %d BinContent= %.2f' % (i-301,bincont)
##
#momentum distribution of the particles matched to VELO

hP = TH1F('mom','',300,0,20000)
t.Project('mom','Particle_P','Track_type == 1')
c3 = TCanvas()
hP.Draw()
heta = TH1F('eta','',500,0,8)
t.Project('eta','Particle_eta','Track_type == 1')
c1 = TCanvas()
heta.Draw()
hphi = TH1F('phi','',20,-np.pi,np.pi)
t.Project('phi','Particle_phi','Track_type == 1')
c2 = TCanvas()
hphi.Draw()

# vou a quitar aqueles eventos q estean na tupla de MatchVeloLong
f2 = TFile('/scratch13/acasais/MatchVeloLong/MatchVeloLong1-40000.root')
t2 = f2.Get('aTree')
hP2=TH1F('mom2','',300,0,20000)
fhist =TFile('Histograma.root','recreate')

event_no = 0
#usar copytree!
for evt in t:
    if event_no != evt.Event_no:
        event_no = evt.Event_no
        tevent = t.CopyTree('Event_no=='+str(event_no))
        t2event = t2.CopyTree('Event_no=='+str(event_no))
    	for ev1 in tevent:
        	for ev2 in t2event:
            		cond2 = '((ev1.Track_px == ev2.Long_px and ev1.Track_py == ev2.Long_py) or (ev1.Track_px == ev2.Velo_px and ev1.Track_py == ev2.Velo_py)'
            		if not cond2:
                                print event_no 
                		hP2.Fill(ev1.Particle_P)
			
			
fhist.cd()
hP2.Write()
fhist.Close()
