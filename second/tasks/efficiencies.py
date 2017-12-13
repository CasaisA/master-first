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

print pack('ola')
    



fup = TFile('/scratch13/acasais/second/KsPiPiee-root/KsPiPiee_up_1-1000000.root')
fdown = TFile('/scratch13/acasais/second/KsPiPiee-root/KsPiPiee_down_1-1000000.root')

tks0t = fup.Get('kS0_truth')
tks0r = fup.Get('ks0products_reco')
treco = fup.Get('pi-e_reco')







    

#calculo de eficiencias
effs= {}
err_eff = {}
max =2000
step = 300
min = 0
no_bins = 10
pTs = range(step,max+step,step)

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

    long2 = 'piplus_trck_type==3 && piminus_trck_type==3'
    long3 = long2+' && '+pack('eplus_trck_type==3 || eminus_trck_type==3')
    long4 = long2+' && '+pack('eplus_trck_type==3 && eminus_trck_type==3')
    
    effs['ks0','long2',pT]=tks0r.GetEntries(long2)/np.float64(tks0t.GetEntries())
    effs['ks0','long3',pT]=tks0r.GetEntries(long3)/np.float64(tks0t.GetEntries())
    effs['ks0','long4',pT]=tks0r.GetEntries(long4)/np.float64(tks0t.GetEntries())

    err_eff['ks0','long2',pT]= m.sqrt(effs['ks0','long2',pT]*(1-effs['ks0','long2',pT])/tks0t.GetEntries())
    err_eff['ks0','long3',pT]= m.sqrt(effs['ks0','long3',pT]*(1-effs['ks0','long3',pT])/tks0t.GetEntries())
    err_eff['ks0','long4',pT]= m.sqrt(effs['ks0','long4',pT]*(1-effs['ks0','long4',pT])/tks0t.GetEntries())
    
    
    min = pT


    
min = 0.
for pT in pTs:
    print 'Eficiencia ks0 (pT entre %.f e %.f Mev): %.4f +- %.4f'%(min,pT,effs['ks0','long2',pT],err_eff['ks0','long2',pT])
    min = pT

#reconstruo algunha masa
final=final.reset_index(drop=True)
ks0_reco = ks0_reco.reset_index(drop=True)
ks0_truth = ks0_truth.reset_index(drop=True)
min = 0
max = 4
m = []
for max in range(4,len(final)+4,4):
    temp = final[(final.index>=min)&(final.index<max)]
    min = max
    #print len(temp)
    if temp['no_long'].values[0]!=4: continue
    px = np.sum(temp['px'].values)
    py = np.sum(temp['py'].values)
    pz = np.sum(temp['pz'].values)
    p2 = px**2+py**2+pz**2
    E = 0
    for i in xrange(len(temp)):
        if abs(temp.iloc()[i]['pid'])==11:
            mi = 0.511
        if abs(temp.iloc()[i]['pid'])==211:
            mi = 139.57
        E+=np.sqrt(temp.iloc()[i]['p']**2+mi**2)
    m.append(np.sqrt(E**2-p2))
    

import matplotlib.pyplot as plt
hist = plt.hist(m,bins=30)
#plt.show()
keys= []
contador = 0
for key in mctruth['evt_id'].values:
    
    if len(mctruth[mctruth.evt_id==key])!=4:
        contador+=1
        #print len(mctruth[mctruth.evt_id==key])
        keys.append(key)
keys = np.unique(keys)

