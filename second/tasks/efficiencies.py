import numpy as np
import pandas as pd
import root_numpy
import root_pandas
import pickle
import matplotlib.pyplot as plt
from scipy.stats import mode
from root_pandas import read_root
from ROOT import * 
# with open('/scratch13/acasais/second/task1/reco-500runs.p') as f:
#     reco = pickle.load(f)

# with open('/scratch13/acasais/second/task1/truth-500runs.p') as f:
#         mctruth = pickle.load(f)


reco = read_root('/scratch13/acasais/second/KsPiPiee-root/KsPiPiee-VELO-long1-1000000.root','reco')
mctruth = read_root('/scratch13/acasais/second/KsPiPiee-root/KsPiPiee-VELO-long1-1000000.root','mctruth')
ks0_truth = read_root('/scratch13/acasais/second/KsPiPiee-root/KsPiPiee-VELO-long1-1000000.root','kS0_truth')
f1 = TFile('/scratch13/acasais/second/KsPiPiee-root/KsPiPiee-VELO-long1-1000000.root')
treco = f1.Get('reco')
ttruth = f1.Get('mctruth')
tks0 = f1.Get('kS0_truth')


#No primeiro paso, de todas as trazas , voume quedar so coas de tipo 1 e 3
selec = reco[((reco.trck_type==1)|(reco.trck_type==3))]
#agora vou a ver cada nai(ks0) que tipos de trazas ten asociadas
key = 0
ks0s={}
for ks0_key in selec['mother_key']:
    if ks0_key==key:
        continue
    temp=selec[(selec.mother_key==ks0_key)]
    ks0s[ks0_key]=list(temp['trck_type'].values) 
    key = ks0_key
#so collo aquelas listas que tenhen 4 trazas polo menos
ks0 ={}
for evt in ks0s.keys():
    if len(ks0s[evt])==4 and ks0s[evt].count(3)>=2:
        ks0[evt]=ks0s[evt]

#construo o dataframe e elimino os duplicados
good = pd.DataFrame()
for key in np.unique(ks0.keys()):
    temp = selec[selec.mother_key==key]
    for i in xrange(len(temp)):
        for j in xrange(i+1,len(temp)):
            if temp.iloc()[i]['px_truth']==temp.iloc()[j]['px_truth'] and temp.iloc()[i]['py_truth']==temp.iloc()[j]['py_truth']:
                break
            if j==len(temp)-1:
                #print i,j
                good = good.append(temp.iloc()[i])                    
    good = good.append(temp.iloc()[len(temp)-1])
candidatos = good

final = pd.DataFrame()
#comprobacion final, miro que en cada lista haxa 11,-11,211,-211

unicos = np.unique(candidatos['mother_key'].values)
for evt in unicos:
    #if key == evt: pass
    #else: 
    temp = candidatos[candidatos.mother_key==evt]
    pids=temp['pid'].values
        
    if (211 in pids and -211 in pids and 11 in pids and -11 in pids):
        final = final.append(temp)
    

final=final.reset_index(drop=True)
#van de 4 en 4 os ks agora no dataframe
for i in np.unique(final['mother_key'].values):
    if len(final[final.mother_key==i])>4:
        temp = final[final.mother_key==i]
        print temp[['pid','px_truth','py_truth','trck_type']]





#AGORA TENHO QUE MIRAR QUE OS DOUS PIONS SENHAN LONG
#no dataframe final tenho un ks0 de 4 en 4 entradas, vou facer agora un dataframe onde tenha so unha entrada por ks0 reco
#as categorias q construo son exclusivas
ks0_reco = pd.DataFrame()
inicio=0
long_pions=pd.DataFrame()
long2=0
long3=0
long4=0
for fin in range(4,len(final)+4,4):
    temp=final[(final.index>=inicio)&(final.index<fin)]
    inicio = fin
    pion = temp[temp.pid==211]
    apion = temp[temp.pid==-211]
    e = temp[temp.pid==11]
    ae = temp[temp.pid==-11]
    pids = temp['pid'].values
    
    if pion.iloc()[0]['trck_type']==3 and apion.iloc()[0]['trck_type']==3 and e.iloc()[0]['trck_type']==3 and ae.iloc()[0]['trck_type']==3:
        long4+=1
        temp['no_long']=4
        long_pions=long_pions.append(temp)
        
    elif pion.iloc()[0]['trck_type']==3 and apion.iloc()[0]['trck_type']==3 and (e.iloc()[0]['trck_type']==3 or ae.iloc()[0]['trck_type']==3):
        long3+=1
        
        temp['no_long']=3
        long_pions=long_pions.append(temp)
        
    elif pion.iloc()[0]['trck_type']==3 and apion.iloc()[0]['trck_type']==3:
        long2+=1
       
        temp['no_long']=2
        long_pions=long_pions.append(temp)
        
    
    if 'no_long' in temp.keys():
        temp1=temp.iloc()[0][['no_long','mother_px','mother_py','mother_pz','mother_p','mother_pT','mother_eta','mother_phi']]
        ks0_reco=ks0_reco.append(temp1)
final = long_pions





    

#calculo de eficiencias
effs= {}
err_eff = {}
max =2000
step = 300
min = 0
no_bins = 10
pTs = range(step,max+step,step)
min = 0
for pT in pTs:
    effs['e','velo',pT]=treco.GetEntries('abs(pid)==11 && trck_type==1 && pT_truth<'+str(pT)+'&&pT_truth>'+str(min))/\
                        np.float64(ttruth.GetEntries('abs(pid)==11 && pT<'+str(pT)+'&&pT>'+str(min)))
    effs['e','long',pT]=treco.GetEntries('abs(pid)==11 && trck_type==3 && pT_truth<'+str(pT)+'&&pT_truth>'+str(min))/\
                        np.float64(ttruth.GetEntries('abs(pid)==11 && pT<'+str(pT)+'&&pT>'+str(min)))
    effs['pi','velo',pT]=treco.GetEntries('abs(pid)==211 && trck_type==1 && pT_truth<'+str(pT)+'&&pT_truth>'+str(min))/\
                        np.float64(ttruth.GetEntries('abs(pid)==211 && pT<'+str(pT)+'&&pT>'+str(min)))
    effs['pi','long',pT]=treco.GetEntries('abs(pid)==211 && trck_type==3 && pT_truth<'+str(pT)+'&&pT_truth>'+str(min))/\
                        np.float64(ttruth.GetEntries('abs(pid)==211 && pT<'+str(pT)+'&&pT>'+str(min)))
    effs['ks0','long2',pT]=len(ks0_reco[(ks0_reco.mother_pT>min)&(ks0_reco.mother_pT<pT)&(ks0_reco.no_long==2)])/\
                            np.float64(len(ks0_truth[(ks0_truth.pT>min)&(ks0_truth.pT<pT)]))
    effs['ks0','long3',pT]=len(ks0_reco[(ks0_reco.mother_pT>min)&(ks0_reco.mother_pT<pT)&(ks0_reco.no_long==3)])/\
                            np.float64(len(ks0_truth[(ks0_truth.pT>min)&(ks0_truth.pT<pT)]))
    effs['ks0','long4',pT]=len(ks0_reco[(ks0_reco.mother_pT>min)&(ks0_reco.mother_pT<pT)&(ks0_reco.no_long==4)])/\
                            np.float64(len(ks0_truth[(ks0_truth.pT>min)&(ks0_truth.pT<pT)]))
    err_eff['e','velo',pT]= np.sqrt(effs['e','velo',pT]*(1-effs['e','velo',pT])/\
                          np.float64(ttruth.GetEntries('abs(pid)==11 && pT<'+str(pT)+'&&pT>'+str(min))))
    err_eff['e','long',pT]= np.sqrt(effs['e','long',pT]*(1-effs['e','long',pT])/\
                            np.float64(ttruth.GetEntries('abs(pid)==11 && pT<'+str(pT)+'&&pT>'+str(min))))
    err_eff['pi','velo',pT]= np.sqrt(effs['pi','velo',pT]*(1-effs['pi','velo',pT])/\
                             np.float64(ttruth.GetEntries('abs(pid)==211 && pT<'+str(pT)+'&&pT>'+str(min))))
    err_eff['pi','long',pT]= np.sqrt(effs['pi','long',pT]*(1-effs['pi','long',pT])/\
                              np.float64(ttruth.GetEntries('abs(pid)==211 && pT<'+str(pT)+'&&pT>'+str(min))))

    err_eff['ks0','long2',pT] = np.sqrt(effs['ks0','long2',pT]*(1-effs['ks0','long2',pT])/\
                                np.float64(len(ks0_truth[(ks0_truth.pT>min)&(ks0_truth.pT<pT)])))
    err_eff['ks0','long2',pT] = np.sqrt(effs['ks0','long3',pT]*(1-effs['ks0','long3',pT])/\
                                np.float64(len(ks0_truth[(ks0_truth.pT>min)&(ks0_truth.pT<pT)])))
    err_eff['ks0','long4',pT] = np.sqrt(effs['ks0','long4',pT]*(1-effs['ks0','long4',pT])/\
                                np.float64(len(ks0_truth[(ks0_truth.pT>min)&(ks0_truth.pT<pT)])))
    min = pT
min = 0.
for pT in pTs:
    print 'Eficiencia ks0 (pT entre %.f e %.f Mev): %.4f +- %.4f'%(min,pT,effs['ks0','long2',pT]+effs['ks0','long3',pT]+effs['ks0','long4',pT],err_eff['ks0','long2',pT])
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
