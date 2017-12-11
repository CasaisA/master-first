# -*- coding: utf-8 -*-
from ROOT import *
import numpy as np
gROOT.ProcessLine(".x /cvmfs/lhcb.cern.ch/lib/lhcb/URANIA/URANIA_v1r1/RootTools/LHCbStyle/src/lhcbStyle.C")
f = TFile('/scratch13/acasais/TrackMatching/TrackMatching1-30000.root')
t = f.Get('aTree')

#Fraction of Velo Tracks
ratio = float(t.GetEntries('Track_type==1'))/t.GetEntries()
#Distribution of the IDs of the mcparticles amtched to VELO tracks

h = TH1F('ID','',600,-300,300)
t.Project('ID','Particle_pid','Track_type == 1')
gStyle.SetOptStat('')
##
c = TCanvas()
h.Draw()
por = 0
for i in xrange(1,600):
    bincont = h.GetBinContent(i)
    if bincont>0:
        print 'MCid= %d BinContent= %.2f' % (i-301,100*bincont/h.GetEntries())
        por += 100*bincont/h.GetEntries()



#momentum distribution of the particles matched to VELO
leg=TLegend(.6,.6,.8,.8)
leg2=TLegend(.6,.6,.8,.8)
leg.SetBorderSize(0)
leg2.SetBorderSize(0)
f2 = TFile('HwoGhosts-notree.root')
hP = TH1F('mom','',300,0,20000)
hP2 = f2.Get('P wo ghosts')
t.Project('mom','Particle_P','Track_type == 1')
c3 = TCanvas()
hP.SetXTitle('p [MeV/c]')
hP.SetYTitle('No. Entries / [67 MeV/c]')
hP2.SetLineColor(kRed)
leg.AddEntry(hP,'raw','L')
leg.AddEntry(hP2,'w/o clons','L')

hP.Draw()
hP2.Draw('same')
leg.Draw()
heta = TH1F('eta','',500,0,8)
heta2= f2.Get('eta wo ghosts')
t.Project('eta','Particle_eta','Track_type == 1')
c1 = TCanvas()
heta.SetXTitle('#eta ')
heta.SetYTitle('No. Entries / 0.016')

heta2.SetLineColor(kRed)

heta.Draw()
heta2.Draw('same')
leg2.AddEntry(hP,'raw','L')
leg2.AddEntry(hP2,'w/o clons','L')
leg2.Draw()
hphi = TH1F('phi','',20,-np.pi,np.pi)
hphi2 = f2.Get('phi wo ghosts')
t.Project('phi','Particle_phi','Track_type == 1')
c2 = TCanvas()
hphi.SetXTitle('#phi')
hphi.SetYTitle('No. Entries / #pi/20')
hphi.Draw()
hphi2.Draw('same')

# f2 = TFile('Histograma.root')
# hP2 =f2.Get('p wo ghosts')
# c4 = TCanvas()
# hP2.Draw()




# #vou a quitar aqueles eventos q estean na tupla de MatchVeloLong
# f2 = TFile('/scratch13/acasais/MatchVeloLong/MatchVeloLong1-40000.root')
# t2 = f2.Get('aTree')
# hP2=TH1F('mom2','',300,0,20000)
# fhist =TFile('Histograma.root')


# # esto vai moi lento 
# event_no = 0
# events=[]
# #usar copytree!
# for evt in t:
#     if event_no != evt.Event_no:
#         events.append(evt.Event_no)
#         event_no = evt.Event_no
# t = t.CopyTree('Track_type==1')        
# event_no = 0
# i = 0
# tevent = TTree()
# t2event = TTree()
# for evt in events:
#     if event_no != evt:
#         fera = TFile('eraseme.root','RECREATE')
#         event_no = evt
#         tevent = t.CopyTree('Event_no=='+str(event_no))
#         t2event = t2.CopyTree('Event_no=='+str(event_no))
#         if t2event.GetEntries()==0 or tevent.GetEntries==0: continue
#     	for ev1 in tevent:
#         	for ev2 in t2event:
#                     if (ev1.Track_px == ev2.Long_px and ev1.Track_py == ev2.Long_py) or\
#                        (ev1.Track_px == ev2.Velo_px and ev1.Track_py == ev2.Velo_px):
                        
                        
#                         continue
#                     else:
                        
#                         hP2.Fill(ev1.Particle_P)
			
			
# fhist.cd()
# hP2.Write()
# fhist.Close()
