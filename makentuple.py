import ROOT
import numpy as np

f = ROOT.TFile('a.root','recreate')
t = ROOT.TTree('aTree','tree title')

#vou a crear arrays unidemensioais
#como variables fill

no = np.zeros(1, dtype=float)
un = np.zeros(1, dtype=float)

#creo as branches

t.Branch('normal',no,'normal/D')
t.Branch('uniform',un,'uniform/D')

for i in xrange(100000):
    no[0] = ROOT.gRandom.Gaus();un[0]= ROOT.gRandom.Uniform()
    t.Fill()

# write the tree into the output file and close
t.Write(); f.Close()
