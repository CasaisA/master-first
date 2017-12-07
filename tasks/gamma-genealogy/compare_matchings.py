import pandas as pd
import pickle
import matplotlib.pyplot as plt

matching_good = pickle.load( open( "matching_bo.p", "rb" ) )
matching_bad = pickle.load( open( "matching_malo.p", "rb" ) )
dR = matching_good['delR'].values
eta = matching_good['trck_eta'].values
#eta2 = matching_good['part_eta'].values
hist = plt.hist(eta,bins=100)
#hist2 = plt.hist(eta2,bins=50)
plt.show()
# pid_coinc = []
# for i,bo in matching_good.iterrows():
# 	for j,bad in matching_bad.iterrows():
# 		if bo['trck_eta'] == bad['trck_eta'] or bo['trck_phi']==bad['trck_phi']:
# 			pid_coinc.append(bo['part_pid'])

# print pid_coinc

# velo_bad = matching_bad['trck_type'].values
# velo_good = matching_good['trck_type'].values
# velo_bad=filter(lambda x: x==1,velo_bad)
# velo_good=filter(lambda x: x==1,velo_good)
# print len(velo_bad)
# print len(velo_good)
# len_pid=len(pid_coinc)
# ratio = len_pid/float(len(filter(lambda x: x==11,pid_coinc)))
# ratio = 1/ratio
# print ratio
# pid_coinc = filter(lambda x: x<300 and x>-300,pid_coinc)
# hist = plt.hist(pid_coinc,bins=len(pid_coinc),range=[-300,300])

# plt.show()
