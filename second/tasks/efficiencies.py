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
# with open('/scratch13/acasais/second/task1/reco-500runs.p') as f:
#     reco = pickle.load(f)

# with open('/scratch13/acasais/second/task1/truth-500runs.p') as f:
#         mctruth = pickle.load(f)

def pack(string):
    return '('+string+')'


    



fup = TFile('/scratch13/acasais/second/KsPiPiee-root/KsPiPiee_up_1-1000000.root')
fdown = TFile('/scratch13/acasais/second/KsPiPiee-root/KsPiPiee_down_1-1000000.root')
f = TFile('/scratch13/acasais/second/KsPiPiee-root/KsPiPiee.root')

tks0t = f.Get('kS0_truth')
tks0r_alltracks = f.Get('ks0products_reco')
treco = f.Get('pi-e_reco')
ferase = TFile('eraseme.root','recreate')
tks0r = tks0r_alltracks.CopyTree('(eminus_trck_type==1||eminus_trck_type==3)&&(eplus_trck_type==1||eplus_trck_type==3)&&(piminus_trck_type==1||piminus_trck_type==3)&&(piplus_trck_type==1||piplus_trck_type==3)')


#calculo de eficiencias
effs= {}
err_eff = {}
max =2000
step = 300
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
    print 'Eficiencia ks0 (pT entre %.f e %.f Mev): %.4f +- %.4f'%(min,pT,effs['ks0','long2',pT],err_eff['ks0','long2',pT])
    min = pT

#reconstruo algunha masa
#por agora so collo os eventos nos que haxa
#catro trazas long
# tlongs = tks0r.CopyTree(long4)
mass = []
# for evt in tlongs:
#     px = evt.eminus_px+evt.eplus_px+evt.piplus_px+evt.piminus_px
#     py = evt.eminus_py+evt.eplus_py+evt.piplus_py+evt.piminus_py
#     pz = evt.eminus_pz+evt.eplus_pz+evt.piplus_pz+evt.piminus_pz
#     p = m.sqrt(px**2+py**2+pz**2)
#     E = m.sqrt(evt.eminus_p**2+0.511**2)+m.sqrt(evt.eplus_p**2+0.511**2)+m.sqrt(evt.piminus_p**2+139.57018**2)+m.sqrt(evt.piplus_p**2+139.57018**2)
#     mass.append(m.sqrt(E**2-p**2))
    

f = TFile('eraseme.root','recreate')
tlong3=tks0r.CopyTree(long3+'&&!'+pack(long4))
for evt in tlong3:
        ux = evt.PV_x-evt.SV_x
        uy = evt.PV_y-evt.SV_y
        uz = evt.PV_z-evt.SV_z
        u = m.sqrt(ux**2+uy**2+uz**2)
        ux= ux/u
        uy = uy/u
        uz = uz/u
        sinthetapiplus = abs(m.sqrt(1-((evt.piplus_px*ux+evt.piplus_py*uy+evt.piplus_pz*uz)/evt.piplus_p)**2))
        sinthetapiminus = abs(m.sqrt(1-((evt.piminus_px*ux+evt.piminus_py*uy+evt.piminus_pz*uz)/evt.piminus_p)**2))
        sinthetaeminus = abs(m.sqrt(1-((evt.eminus_px*ux+evt.eminus_py*uy+evt.eminus_pz*uz)/evt.eminus_p)**2))
        sinthetaeplus = abs(m.sqrt(1-((evt.eplus_px*ux+evt.eplus_py*uy+evt.eplus_pz*uz)/evt.eplus_p)**2))
        ptpiplus = evt.piplus_p*sinthetapiplus
        ptpiminus = evt.piminus_p*sinthetapiminus
        
        if evt.eplus_trck_type == 1:
            pteminus = evt.eminus_p*sinthetaeminus
            pteplus = -pteminus-ptpiminus-ptpiplus
            pe=abs(pteplus/sinthetaeplus)
            eplus_px = pe*evt.eplus_px/evt.eplus_p
            eplus_py = pe*evt.eplus_py/evt.eplus_p
            eplus_pz = pe*evt.eplus_pz/evt.eplus_p

            eminus_px = evt.eminus_px
            eminus_py = evt.eminus_py
            eminus_pz = evt.eminus_pz
        
        if evt.eminus_trck_type == 1:
            pteplus = evt.eplus_p*sinthetaeplus
            pteminus = -pteplus-ptpiminus-ptpiplus
            pe=abs(pteminus/sinthetaeminus)
            eminus_px = pe*evt.eminus_px/evt.eminus_p
            eminus_py = pe*evt.eminus_py/evt.eminus_p
            eminus_pz = pe*evt.eminus_pz/evt.eminus_p

            eplus_px = evt.eplus_px
            eplus_py = evt.eplus_py
            eplus_pz = evt.eplus_pz
        else:
            eminus_px = evt.eminus_px
            eminus_py = evt.eminus_py
            eminus_pz = evt.eminus_pz

            eplus_px = evt.eplus_px
            eplus_py = evt.eplus_py
            eplus_pz = evt.eplus_pz
        
            

        px = eminus_px+eplus_px+evt.piplus_px+evt.piminus_px
        py = eminus_py+eplus_py+evt.piplus_py+evt.piminus_py
        pz = eminus_pz+eplus_pz+evt.piplus_pz+evt.piminus_pz
        eminus_p = m.sqrt(eminus_px**2+eminus_py**2+eminus_pz**2)
        eplus_p = m.sqrt(eplus_px**2+eplus_py**2+eplus_pz**2)
        p = m.sqrt(px**2+py**2+pz**2)
        E = m.sqrt(eminus_p**2+0.511**2)+m.sqrt(eplus_p**2+0.511**2)+m.sqrt(evt.piminus_p**2+139.57018**2)+m.sqrt(evt.piplus_p**2+139.57018**2)
        mass.append(m.sqrt(E**2-p**2))
import matplotlib.pyplot as plt
hist = plt.hist(mass,bins=50)
plt.show()
