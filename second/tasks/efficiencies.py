
import numpy as np
import math as m
# import pandas as pd
# import root_numpy
# import root_pandas
# import pickle
import matplotlib.pyplot as plt
# from scipy.stats import mode
# from root_pandas import read_root
from ROOT import *
from easygraphs import *
gROOT.ProcessLine(".x /cvmfs/lhcb.cern.ch/lib/lhcb/URANIA/URANIA_v1r1/RootTools/LHCbStyle/src/lhcbStyle.C")
# with open('/scratch13/acasais/second/task1/reco-500runs.p') as f:
#     reco = pickle.load(f)

# with open('/scratch13/acasais/second/task1/truth-500runs.p') as f:
#         mctruth = pickle.load(f)

def pack(string):
    return '('+string+')'


    



#fup = TFile('/scratch13/acasais/second/KsPiPiee-root/KsPiPiee_up_1-1000000.root')
#fdown = TFile('/scratch13/acasais/second/KsPiPiee-root/KsPiPiee_down_1-1000000.root')
f = TFile('/scratch13/acasais/second/KsPiPiee-root/updown_all.root')
#f = TFile('/scratch13/acasais/second/KsPiPiee-root/KsPiPiee.root')


tks0t = f.Get('kS0_truth')
tks0r_alltracks = f.Get('ks0products_reco')
treco = f.Get('pi-e_reco')
ferase = TFile('eraseme.root','recreate')
tks0r = tks0r_alltracks.CopyTree('(eminus_trck_type==1||eminus_trck_type==3)&&(eplus_trck_type==1||eplus_trck_type==3)&&(piminus_trck_type==1||piminus_trck_type==3)&&(piplus_trck_type==1||piplus_trck_type==3)')


#calculo de eficiencias
effs= {}
err_eff = {}
max =500
step = 10
min = 0
no_bins = 10
pTs = range(step,max+step,step)

long2 = 'piplus_trck_type==3 && piminus_trck_type==3'
long3 = long2+' && '+pack('eplus_trck_type==3 || eminus_trck_type==3')
long4 = long2+' && '+pack('eplus_trck_type==3 && eminus_trck_type==3')
    
for pT in pTs:
    max = pT
    no_ents_e = np.float64(tks0t.GetEntries(pack('eminus_pT>'+str(min)+'&& eminus_pT<'+str(max))+'||'+pack('eplus_pT>'+str(min)+'&&eplus_pT<'+str(max))))
    no_dous_e = np.float64(tks0t.GetEntries(pack('eminus_pT>'+str(min)+'&& eminus_pT<'+str(max))+'&&'+pack('eplus_pT>'+str(min)+'&&eplus_pT<'+str(max))))
    no_e_truth = np.float64(2*no_dous_e+(no_ents_e-no_dous_e))

    no_ents_pi = np.float64(tks0t.GetEntries(pack('piminus_pT>'+str(min)+'&& piminus_pT<'+str(max))+'||'+pack('piplus_pT>'+str(min)+'&&piplus_pT<'+str(max))))
    no_dous_pi = np.float64(tks0t.GetEntries(pack('piminus_pT>'+str(min)+'&& piminus_pT<'+str(max))+'&&'+pack('piplus_pT>'+str(min)+'&&piplus_pT<'+str(max))))
    no_pi_truth = np.float64(2*no_dous_pi+(no_ents_pi-no_dous_pi))
    
    
    effs['e','velo',pT]= treco.GetEntries('abs(pid)==11 && trck_type==1 && pT_truth>'+str(min)+' && pT_truth<'+str(max))/no_e_truth
    effs['e','long',pT]= treco.GetEntries('abs(pid)==11 && trck_type==3 && pT_truth>'+str(min)+' && pT_truth<'+str(max))/no_e_truth

    effs['pi','velo',pT]= treco.GetEntries('abs(pid)==211 && trck_type==1 && pT_truth>'+str(min)+' && pT_truth<'+str(max))/no_pi_truth
    effs['pi','long',pT]= treco.GetEntries('abs(pid)==211 && trck_type==3 && pT_truth>'+str(min)+' && pT_truth<'+str(max))/no_pi_truth

    err_eff['e','velo',pT]= m.sqrt(effs['e','velo',pT]*(1-effs['e','velo',pT])/no_e_truth)
    err_eff['e','long',pT]= m.sqrt(effs['e','long',pT]*(1-effs['e','long',pT])/no_e_truth)

    err_eff['pi','velo',pT]= m.sqrt(effs['pi','velo',pT]*(1-effs['pi','velo',pT])/no_e_truth)
    err_eff['pi','long',pT]= m.sqrt(effs['pi','long',pT]*(1-effs['pi','long',pT])/no_e_truth)

    
    effs['ks0','long2',pT]=tks0r.GetEntries(pack(long2)+' && pT_truth < '+str(max)+' && pT_truth > '+str(min))/\
                            np.float64(tks0t.GetEntries('pT < '+str(max)+' && pT > '+str(min)))
    effs['ks0','long3',pT]=tks0r.GetEntries(pack(long3)+' && pT_truth < '+str(max)+' && pT_truth > '+str(min))/\
                            np.float64(tks0t.GetEntries('pT < '+str(max)+' && pT > '+str(min)))
    effs['ks0','long4',pT]=tks0r.GetEntries(pack(long4)+' && pT_truth < '+str(max)+' && pT_truth > '+str(min))/\
                            np.float64(tks0t.GetEntries('pT < '+str(max)+' && pT > '+str(min)))

    err_eff['ks0','long2',pT]= m.sqrt(effs['ks0','long2',pT]*(1-effs['ks0','long2',pT])/\
                               np.float64(tks0t.GetEntries('pT < '+str(max)+' && pT > '+str(min))))       
    err_eff['ks0','long3',pT]= m.sqrt(effs['ks0','long3',pT]*(1-effs['ks0','long3',pT])/\
                               np.float64(tks0t.GetEntries('pT < '+str(max)+' && pT > '+str(min))))
                                      
    err_eff['ks0','long4',pT]= m.sqrt(effs['ks0','long4',pT]*(1-effs['ks0','long4',pT])/\
                               np.float64(tks0t.GetEntries('pT < '+str(max)+' && pT > '+str(min))))
    
    
    min = pT


    
min = 0.
for pT in pTs:
    print 'Eficiencia ks0 (pT entre %.f e %.f Mev): %.4f +- %.4f'%(min,pT,effs['ks0','long3',pT],err_eff['ks0','long3',pT])
    min = pT
#parte auxiliar para facer uns graficos 
parts = ['e','pi']
tracks=['velo']
g = []
c = []
for particle in parts:
    for track in tracks:
        values = map(lambda x: effs[particle,track,x],pTs)
        errors_y = map(lambda x: err_eff[particle,track,x],pTs)
        errors_x = list(np.zeros(len(values)))
        g = graph(pTs,values,errors_x,errors_y)
        g.GetYaxis().SetTitle('#epsilon('+particle+'_{'+track+'})')
        g.GetXaxis().SetTitle('pT [MeV]')
        
        g.Draw('same AP')

g = graph()
#reconstruo algunha masa
#por agora so collo os eventos nos que haxa
#catro trazas long

tlong4 = tks0r.CopyTree(long4)
mass_4 = []
for evt in tlong4:
    px = evt.eminus_px+evt.eplus_px+evt.piplus_px+evt.piminus_px
    py = evt.eminus_py+evt.eplus_py+evt.piplus_py+evt.piminus_py
    pz = evt.eminus_pz+evt.eplus_pz+evt.piplus_pz+evt.piminus_pz
    p = m.sqrt(px**2+py**2+pz**2)
    E = m.sqrt(evt.eminus_p**2+0.511**2)+m.sqrt(evt.eplus_p**2+0.511**2)+m.sqrt(evt.piminus_p**2+139.57018**2)+m.sqrt(evt.piplus_p**2+139.57018**2)
    mass_4.append(m.sqrt(E**2-p**2))



    

f1 = TFile('eraseme.root','recreate')
tlong3=tks0r.CopyTree(long3)
e_recons = {}
e_truth = {}
massalt=[]
mass_3=[]
mass_3muon=[]
for evt in tlong3:
    
        ux = evt.SV_x-evt.PV_x
        uy = evt.SV_y-evt.PV_y
        uz = evt.SV_z-evt.PV_z

        u = m.sqrt(ux**2+uy**2+uz**2)
        ux= ux/u
        uy = uy/u
        uz = uz/u
        #uprim e uprima, o vector resultante dos outros tres, que ten q ser coplanario co momento do electron/positron
        uprim_x = evt.piplus_px+evt.piminus_px
        uprim_y = evt.piplus_py+evt.piminus_py
        uprim_z = evt.piplus_pz+evt.piminus_pz
        if evt.eplus_trck_type == 1:
            uprim_x+=evt.eminus_px
            uprim_y+=evt.eminus_py
            uprim_z+=evt.eminus_pz
            uprim = m.sqrt(uprim_x**2+uprim_y**2+uprim_z**2)
            costhetaeplus = (ux*evt.eplus_px + uy*evt.eplus_py + uz*evt.eplus_pz)/evt.eplus_p
            sinthetaeplus = m.sqrt(1-costhetaeplus**2)
            costhetauprim= (ux*uprim_x + uy*uprim_y + uz*uprim_z)/uprim
            sinthetauprim = m.sqrt(1-costhetauprim**2)

            pe=uprim*sinthetauprim/sinthetaeplus
            
            eplus_px = pe*evt.eplus_px/evt.eplus_p
            eplus_py = pe*evt.eplus_py/evt.eplus_p
            eplus_pz = pe*evt.eplus_pz/evt.eplus_p

           

            

            v0 = TVector3(eplus_px,eplus_py,eplus_pz)
            v1 = TVector3(evt.eplus_px_truth,evt.eplus_py_truth,evt.eplus_pz_truth)

            eminus_px = evt.eminus_px
            eminus_py = evt.eminus_py
            eminus_pz = evt.eminus_pz

            px = eminus_px+eplus_px+evt.piplus_px+evt.piminus_px
            py = eminus_py+eplus_py+evt.piplus_py+evt.piminus_py
            pz = eminus_pz+eplus_pz+evt.piplus_pz+evt.piminus_pz
            eminus_p = m.sqrt(eminus_px**2+eminus_py**2+eminus_pz**2)
            eplus_p = m.sqrt(eplus_px**2+eplus_py**2+eplus_pz**2)
        
            E = m.sqrt(eminus_p**2+0.511**2)+m.sqrt(eplus_p**2+0.511**2)+m.sqrt(evt.piminus_p**2+139.57018**2)+m.sqrt(evt.piplus_p**2+139.57018**2)
            Emuon= m.sqrt(eminus_p**2+105.568**2)+m.sqrt(eplus_p**2+0.511**2)+m.sqrt(evt.piminus_p**2+139.57018**2)+m.sqrt(evt.piplus_p**2+139.57018**2)
            v2 = TLorentzVector(px,py,pz,E)
            v2muon = TLorentzVector(px,py,pz,Emuon)
            mass_3.append(v2.M())
            mass_3muon.append(v2muon.M())
            
        
        elif evt.eminus_trck_type == 1:
            uprim_x+=evt.eplus_px
            uprim_y+=evt.eplus_py
            uprim_z+=evt.eplus_pz
            uprim = m.sqrt(uprim_x**2+uprim_y**2+uprim_z**2)
            costhetaeminus = (ux*evt.eminus_px + uy*evt.eminus_py + uz*evt.eminus_pz)/evt.eminus_p
            sinthetaeminus = m.sqrt(1-costhetaeminus**2)
            costhetauprim= (ux*uprim_x + uy*uprim_y + uz*uprim_z)/uprim
            sinthetauprim = m.sqrt(1-costhetauprim**2)

            pe=uprim*sinthetauprim/sinthetaeminus

            
            eminus_px = pe*evt.eminus_px/evt.eminus_p
            eminus_py = pe*evt.eminus_py/evt.eminus_p
            eminus_pz = pe*evt.eminus_pz/evt.eminus_p

            
            
            

            v0 = TVector3(eminus_px,eminus_py,eminus_pz)
            v1 = TVector3(evt.eminus_px_truth,evt.eminus_py_truth,evt.eminus_pz_truth)
            
            eplus_px = evt.eplus_px
            eplus_py = evt.eplus_py
            eplus_pz = evt.eplus_pz
        
        
            
        
            px = eminus_px+eplus_px+evt.piplus_px+evt.piminus_px
            py = eminus_py+eplus_py+evt.piplus_py+evt.piminus_py
            pz = eminus_pz+eplus_pz+evt.piplus_pz+evt.piminus_pz
            eminus_p = m.sqrt(eminus_px**2+eminus_py**2+eminus_pz**2)
            eplus_p = m.sqrt(eplus_px**2+eplus_py**2+eplus_pz**2)
        
            E = m.sqrt(eminus_p**2+0.511**2)+m.sqrt(eplus_p**2+0.511**2)+m.sqrt(evt.piminus_p**2+139.57018**2)+m.sqrt(evt.piplus_p**2+139.57018**2)
            Emuon= m.sqrt(eminus_p**2+0.511**2)+m.sqrt(eplus_p**2+105.658**2)+m.sqrt(evt.piminus_p**2+139.57018**2)+m.sqrt(evt.piplus_p**2+139.57018**2)
            v2 = TLorentzVector(px,py,pz,E)
            v2muon = TLorentzVector(px,py,pz,Emuon)
            mass_3.append(v2.M())
            mass_3muon.append(v2muon.M())

        else:
            
            eplus_px = evt.eplus_px
            eplus_py = evt.eplus_py
            eplus_pz = evt.eplus_pz

            eminus_px = evt.eminus_px
            eminus_py = evt.eminus_py
            eminus_pz = evt.eminus_pz

            px = eminus_px+eplus_px+evt.piplus_px+evt.piminus_px
            py = eminus_py+eplus_py+evt.piplus_py+evt.piminus_py
            pz = eminus_pz+eplus_pz+evt.piplus_pz+evt.piminus_pz
            eminus_p = m.sqrt(eminus_px**2+eminus_py**2+eminus_pz**2)
            eplus_p = m.sqrt(eplus_px**2+eplus_py**2+eplus_pz**2)
        
            E = m.sqrt(eminus_p**2+0.511**2)+m.sqrt(eplus_p**2+0.511**2)+m.sqrt(evt.piminus_p**2+139.57018**2)+m.sqrt(evt.piplus_p**2+139.57018**2)
            Emuon= m.sqrt(eminus_p**2+0.511**2)+m.sqrt(eplus_p**2+105.658**2)+m.sqrt(evt.piminus_p**2+139.57018**2)+m.sqrt(evt.piplus_p**2+139.57018**2)
            v2 = TLorentzVector(px,py,pz,E)
            v2muon = TLorentzVector(px,py,pz,Emuon)
            mass_3.append(v2.M())
            mass_3muon.append(v2muon.M())

#agora 
fera=TFile('eraseme.root','recreate')
tlong2 = tks0r.CopyTree(long2+'&& !'+pack(long3)+'&& !'+pack(long4))
mlong2 = []
for evt in tlong2:
        
        ux = evt.SV_x-evt.PV_x
        uy = evt.SV_y-evt.PV_y
        uz = evt.SV_z-evt.PV_z

        u = TVector3(ux,uy,uz)
        u.SetMag(1.)
        #uprim e uprima, o vector resultante dos outros tres, que ten q ser coplanario co momento do electron/positron
        uprim_x = evt.piplus_px+evt.piminus_px
        uprim_y = evt.piplus_py+evt.piminus_py
        uprim_z = evt.piplus_pz+evt.piminus_pz
        
           
        uprim = TVector3(uprim_x,uprim_y,uprim_z)
        peplus = TVector3(evt.eplus_px,evt.eplus_py,evt.eplus_pz)
        peplus.SetMag(1.)
        peminus = TVector3(evt.eminus_px,evt.eminus_py,evt.eminus_pz)
        peminus.SetMag(1.)
        pe = peplus + peminus
        #o angulo da resultante dos dous pions/electrons con respecto a incidente de ks0
        sinthetauprim=m.sin(u.Angle(uprim))
        sinthetae = m.sin(u.Angle(pe))
        pe.SetMag(uprim.Mag()*sinthetauprim/sinthetae)
        costhetaeplus = m.cos(peplus.Angle(pe))
        costhetaeminus = m.cos(peminus.Angle(pe))
        peplus.SetMag(pe.Mag()/(costhetaeplus+costhetaeminus))
        peminus.SetMag(peplus.Mag())
        p4piplus =TLorentzVector()
        p4piplus.SetXYZM(evt.piplus_px,evt.piplus_py,evt.piplus_pz,139.57)
        p4piminus =TLorentzVector()
        p4piminus.SetXYZM(evt.piminus_px,evt.piminus_py,evt.piminus_pz,139.57)
        p4eminus = TLorentzVector()
        p4eminus.SetVectM(peminus,0.511)
        p4eplus = TLorentzVector()
        p4eplus.SetVectM(peplus,0.511)
        p4ks0 = p4piplus+p4piminus+p4eminus+p4eplus
        mlong2.append(p4ks0.M())
        
        

         











leg=TLegend(.6,.6,.8,.8)
#h0=hlong3
h0 = TH1F('masa ks01','masa ks01',50,300,1000.0)
leg.AddEntry(h0,'3 longs','L')
for mas in mass_3:
    h0.Fill(mas)
c0 = TCanvas()
h0.SetXTitle('M(K_{S}^{0})[MeV/c^{2}]')
h0.SetYTitle('No.Entries / 20 MeV/c^{2}')
h0.DrawNormalized()





#h = hlong4
h = TH1F('masa ks0','masa ks0',50,300,1000.0)
leg.AddEntry(h,'4 longs','L')
for mas in mass_4:
    h.Fill(mas)

#h.SetXTitle('M(K_{S}^{0})[MeV/c^{2}]')
#h.SetYTitle('No.Entries / 20 MeV/c^{2}')
h.SetLineColor(kRed)
h.DrawNormalized('same')
leg.Draw()


hlong2 = TH1F('masa ks0long2','masa ks0long2',50,300,1000.0)
leg.AddEntry(hlong2,'2 longs','L')
for mas in mlong2:
    hlong2.Fill(mas)
#clong2 = TCanvas()
hlong2.SetXTitle('M(K_{S}^{0})[MeV/c^{2}]')
hlong2.SetYTitle('No.Entries / 20 MeV/c^{2}')
hlong2.SetLineColor(kBlue)
hlong2.DrawNormalized('same')  

##Resolucion en momento para os pions/electrons

##uso a formula do ano pasado deltaP/ptruth
#esto que pego aqui e o script do ano pasado
x = []
y = []
c = TCanvas()
i = 0
j = 0
while i < 100 and j<100:
#	print 'i= ' + str(i)
#	print 'j= ' + str(j)
	j = j +1
	cond = 'abs(eminus_p)>'+str(i)+'e2 && abs(eminus_p)<('+str(i)+'e2+'+str(j)+'e2)&& eminus_trck_type==3'
	if tks0r.GetEntries(cond)>1:
		h1=TH1F('h','',100,0,7e4)
		tks0r.Project('h','abs((eminus_p-eminus_p_truth)/eminus_p_truth)',cond)
		x.append((i+j)*100/2.)
        	y.append(h1.GetStdDev())
		i = j
		h1 = 0
	
 
	else:
		j = j+1
	
g = graph(x,y)
g.GetYaxis().SetTitle('#sigma(#Delta p/p_{truth})')
g.GetXaxis().SetTitle('p (MeV/c)')
g.Draw('AP')
    

x = []
y = []

i = 0
j = 0
while i < 100 and j<100:
#	print 'i= ' + str(i)
#	print 'j= ' + str(j)
	j = j +1
	cond = 'abs(piminus_p)>'+str(i)+'e2 && abs(piminus_p)<('+str(i)+'e2+'+str(j)+'e2)&& piminus_trck_type==3'
	if tks0r.GetEntries(cond)>1:
		h1=TH1F('h','',100,0,7e4)
		tks0r.Project('h','abs((piminus_p-piminus_p_truth)/piminus_p_truth)',cond)
		x.append((i+j)*100/2.)
        	y.append(h1.GetStdDev())
		i = j
		h1 = 0
	
 
	else:
		j = j+1
	
g1 = graph(x,y)
g1.GetYaxis().SetTitle('#sigma(#Delta p/p_{truth})')
g1.GetXaxis().SetTitle('p (MeV/c)')
g1.Draw('same AP')







    
    

        
    
