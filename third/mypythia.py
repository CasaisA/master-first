from numpythia import Pythia, ABS_PDG_ID

#selection = ( (ABS_PDG_ID == 310) )
params = {
 "softQCD:all": "on",
 "Beams:eCM": 13000}


# dtype=[('E', '<f8'), ('px', '<f8'), ('py', '<f8'), ('pz', '<f8'), ('mass', '<f8'), ('prodx', '<f8'), ('prody', '<f8'), ('prodz', '<f8'), ('prodt', '<f8'), ('pdgid', '<i4'), ('status', '<i4')])
i=0
out = []
for event in Pythia(params=params):
   ks0s = filter(lambda x: x[-2]==310,event.all())
   if len(ks0s): out.extend(ks0s);i+=1
   if i==100: break


## ASSUME KS0S COME FROM X,Y,Z = 0, 0, 0
## DECAY THEM FOLLOWING PROPER LIFETIME EXPONENTIAL DECAY:
## TAKE KS0 LIFETIME. WITH EXPONENTIAL DISTRIBUTION, DETERMINE (RANDOM) LIFETIME (EXPLORE TRandom3 in ROOT) TRandom3().Expo(life)
## CALCULATE DECAY POINT (USE BOOST)

## ALEXANDRE
## plot fraction in theta<400, z decay<500 mm for 8,13,14,27 TeV for k+, ks, sigma, lambda

## ADRIAN
## DECAY THEM WITH ROOT TGenPhaseSpace (setDecay to pipiee)
## THEN SMEAR MOMENTUM OF PIONS ACCORDING TO LHCB RESOLUTION, USE 1% FOR PIONS AND 5% FOR ELECTRONS. USE TRandom3().Gauss(momento_true,reso)
## COMPUTE KS0 MASS IN BOTH CASES. (RECO WITH STANDARD MASS, AFTER USING 'TRICK')
