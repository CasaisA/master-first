# -*- coding: utf-8 -*-
from ROOT import *


f = TFile('/scratch13/acasais/TrackMatching/merged.root')
t = f.Get('aTree')

#Fraction of Velo Tracks
ratio = float(t.GetEntries('Track_type==1'))/t.GetEntries()

#Distribution of the IDs of the mcparticles amtched to VELO tracks

h = TH1F('test','',600,-300,300)
t.Project('test','Particle_pid','Track_type == 3')
c = TCanvas()
h.Draw()
for i in xrange(1,600):
    bincont = h.GetBinContent(i)
    if bincont>0:
        print 'MCid= %d BinContent= %.2f' % (i-301,bincont)

