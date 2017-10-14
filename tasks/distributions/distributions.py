# -*- coding: utf-8 -*-
from ROOT import *
import numpy as np

f = TFile('/scratch13/acasais/TrackMatching/TrackMatching1-5000.root')
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
heta = TH1F('eta','',300,0,8)
t.Project('eta','Particle_eta','Track_type == 1')
c1 = TCanvas()
heta.Draw()
hphi = TH1F('phi','',10,-np.pi,np.pi)
t.Project('phi','Particle_phi','Track_type == 1')
c2 = TCanvas()
hphi.Draw()

