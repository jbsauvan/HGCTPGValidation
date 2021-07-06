#######################################################################################################################
# Read a file with the information from MemoryCheck and Time and fill corresponding histo (Nbr/Time/event)
# for each producer HGCalVFEProducer, HGCalConcentratorProducer, HGCalBackendLayer1Producer, HGCalBackendLayer2Producer,
# HGCalTowerMapProducer and HGCalTowerProducer

import os
import sys

from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F
from ROOT import gROOT, gBenchmark, gRandom, gSystem, gDirectory, Double

def readFileStatement(namefile, dirname):
    # for test
    f= open("test_resizeHistos.txt","a+")
    f.write('Open test_resizeHistos.txt')
    print('dirname = ', dirname)
    # Name of the file containing histograms
    rootFileName = "/DQM_V0001_R000000001__validation__HGCAL__TPG.root"
    rootFile = dirname + '/' + rootFileName

    # Open existing ROOT file
    hFile = TFile( rootFile, 'UPDATE' )
    # Places into the directory containing histograms
    topDir = gDirectory
    topDir.cd("DQMData/Run 1/HGCALTPG/Run summary")
    
    h_VFE = TH1F( 'h_VFE', 'HGCalVFEProducer: Time/event distribution', 100, 0, 1.5 )
    h_Conc = TH1F( 'h_Conc', 'HGCalConcentratorProducer: Time/event distribution', 100, 0, 2.5 )
    h_BackendL1 = TH1F( 'h_BackendL1', 'HGCalBackendLayer1Producer: Time/event distribution', 100, 0, 1.5 )
    h_BackendL2 = TH1F( 'h_BackendL2', 'HGCalBackendLayer2Producer: Time/event distribution', 100, 0, 1.5 )
    h_TowerMap = TH1F( 'h_TowerMap', 'HGCalTowerMapProducer: Time/event distribution', 100, 0, 0.5 )
    h_Tower = TH1F( 'h_Tower', 'HGCalTowerProducer: Time/event distribution', 100, 0, 0.5 )
    # list of histograms
    listHistos = [h_VFE, h_Conc, h_BackendL1, h_BackendL2, h_TowerMap, h_Tower]

    # list containing all name if producers
    listProducers=['HGCalVFEProducer', 'HGCalConcentratorProducer','HGCalBackendLayer1Producer','HGCalBackendLayer2Producer', 'HGCalTowerMapProducer','HGCalTowerProducer']
 
    # Open TimingInfo_.txt
    f.write(namefile)
    with open(namefile) as file:
        # Read data in the file
        data = file.readlines()
        for line in data:
            # Split a line and loop over it
            words=line.split()
            for i in range(len(listProducers)):
                if words[4]==listProducers[i]:
                    listHistos[i].Fill(float(words[5]))
    # Set new histo range, -10% bellow the first non zero bin, and + 10% above the last non zero bin
    for i in range(len(listProducers)):
        if (listHistos[i].FindFirstBinAbove() <> listHistos[i].FindLastBinAbove()):
            add = int(listHistos[i].FindLastBinAbove()*0.10)
            if (add == 0):
                add = 5
            listHistos[i].GetXaxis().SetRange(listHistos[i].FindFirstBinAbove() - add, listHistos[i].FindLastBinAbove() + add)
        elif (listHistos[i].FindLastBinAbove() == 1):
            listHistos[i].GetXaxis().SetRange(listHistos[i].FindFirstBinAbove(), listHistos[i].FindLastBinAbove() + 10)
    hFile.Write()
    f.close()

def main(reffile, testfile, refdir, testdir):
    print('reffile = \n', reffile)
    readFileStatement(reffile, refdir)
    readFileStatement(testfile, testdir)

if __name__== "__main__":
    import optparse
    import importlib
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--reffile', dest='reffile', help=' ', default='')
    parser.add_option('--testfile', dest='testfile', help=' ', default='')
    parser.add_option('--refdir', dest='refdir', help=' ', default='')
    parser.add_option('--testdir', dest='testdir', help=' ', default='')
    (opt, args) = parser.parse_args()

    main(opt.reffile, opt.testfile, opt.refdir, opt.testdir)
