import os
import sys

from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F
from ROOT import gROOT, gBenchmark, gRandom, gSystem, gDirectory, Double


histograms = [
  TH1F("tc_n", "trigger cell number; number", 500, 10000, 25000),
  TH1F("tc_mipPt", "trigger cell mipPt; mipPt", 500, 0, 100),
  TH1F("tc_pt", "trigger cell pt; pt [GeV]", 500, 0, 5),
  TH1F("tc_energy", "trigger cell energy; energy [GeV]", 500, 0, 100),
  TH1F("tc_eta", "trigger cell eta; eta", 60, -3.14, 3.14),
  TH1F("tc_phi", "trigger cell phi; phi", 60, -3.14, 3.14),
  TH1F("tc_x", "trigger cell x; x [cm]", 500, -250, 250),
  TH1F("tc_y", "trigger cell y; y [cm]", 500, -250, 250),
  TH1F("tc_z", "trigger cell z; z [cm]", 1100, -550, 550),
  TH1F("tc_layer", "trigger cell layer; layer", 50, 0, 50),

  # cluster 2D histograms
  #  TH1F("cl_n", "cluster2D number; number", 80, 0, 80),
  #  TH1F("cl_mipPt", "cluster2D mipPt; mipPt", 600, 0, 600),
  #  TH1F("cl_pt", "cluster2D pt; pt [GeV]", 20, 0, 20),
  #  TH1F("cl_energy", "cluster2D energy; energy [GeV]", 80, 0, 80),
  #  TH1F("cl_eta", "cluster2D eta; eta", 60, -3.14, 3.14),
  #  TH1F("cl_phi", "cluster2D phi; phi", 60, -3.14, 3.14),
  #  TH1F("cl_cells_n", "cluster2D cells_n; cells_n", 16, 0, 16),
  #  TH1F("cl_layer", "cluster2D layer; layer", 50, 0, 50),

  # multiclusters
  TH1F("cl3d_n", "cl3duster3D number; number", 12, 0, 12),
  TH1F("cl3d_pt", "cl3duster3D pt; pt [GeV]", 50, 0, 50),
  TH1F("cl3d_energy", "cl3duster3D energy; energy [GeV]", 80, 0, 80),
  TH1F("cl3d_eta", "cl3duster3D eta; eta", 60, -3.14, 3.14),
  TH1F("cl3d_phi", "cl3duster3D phi; phi", 60, -3.14, 3.14),
  TH1F("cl3d_clusters_n", "cl3duster3D clusters_n; clusters_n", 30, 0, 30),
  # cluster shower shapes
  TH1F("cl3d_showerlength", "cl3duster3D showerlength; showerlength", 50, 0, 50),
  TH1F("cl3d_coreshowerlength", "cl3duster3D coreshowerlength; coreshowerlength", 16, 0, 16),
  TH1F("cl3d_firstlayer", "cl3duster3D firstlayer; firstlayer", 50, 0, 50),
  TH1F("cl3d_maxlayer", "cl3duster3D maxlayer; maxlayer", 50, 0, 50),
  TH1F("cl3d_seetot", "cl3duster3D seetot; seetot", 50, 0, 0.05),
  TH1F("cl3d_seemax", "cl3duster3D seemax; seemax", 40, 0, 0.04),
  TH1F("cl3d_spptot", "cl3duster3D spptot; spptot", 800, 0, 0.08),
  TH1F("cl3d_sppmax", "cl3duster3D sppmax; sppmax", 800, 0, 0.08),
  TH1F("cl3d_szz", "cl3duster3D szz; szz", 50, 0, 50),
  TH1F("cl3d_srrtot", "cl3duster3D srrtot; srrtot", 800, 0, 0.008),
  TH1F("cl3d_srrmax", "cl3duster3D srrmax; srrmax", 900, 0, 0.009),
  TH1F("cl3d_srrmean", "cl3duster3D srrmean; srrmean", 800, 0, 0.008),
  TH1F("cl3d_emaxe", "cl3duster3D emaxe; emaxe", 15, 0, 1.5),
  TH1F("cl3d_bdteg", "cl3duster3D bdteg; bdteg", 30, -0.7, 0.4),
  TH1F("cl3d_quality", "cl3duster3D quality; quality", 20, 0, 2),

  # towers
  TH1F("tower_n", "tower n; number", 400, 1200, 1600),
  TH1F("tower_pt", "tower pt; pt [GeV]", 50, 0, 50),
  TH1F("tower_energy", "tower energy; energy [GeV]", 200, 0, 200),
  TH1F("tower_eta", "tower eta; eta", 60, -3.14, 3.14),
  TH1F("tower_phi", "tower phi; phi", 60, -3.14, 3.14),
  TH1F("tower_etEm", "tower etEm; etEm", 50, 0, 50),
  TH1F("tower_etHad", "tower etHad; etHad", 30, 0, 0.3),
  TH1F("tower_iEta", "tower iEta; iEta", 20, 0, 20),
  TH1F("tower_iPhi", "tower iPhi; iPhi", 80, 0, 80),
  ]

def createHistograms(namefile, dirname):
    inputFile = TFile(dirname + '/' + namefile)
    tree = inputFile.Get("hgcalTriggerNtuplizer/HGCalTriggerNtuple")
    filledHistograms = []
    for histo in histograms:
      varName = histo.GetName()
      tree.Draw(varName+'>>'+varName, "", "goff")
      filledHistograms.append(gDirectory.Get(varName))


    # Name of the file containing histograms
    outputFileName = "/DQM_V0001_R000000001__validation__HGCAL__TPG.root"
    outputFile = TFile(dirname + '/' + outputFileName, "RECREATE")
    # Places into the directory containing histograms
    topDir = gDirectory
    cddir = topDir.mkdir("DQMData")
    cddir = cddir.mkdir("Run 1")
    cddir = cddir.mkdir("HGCALTPG")
    cddir = cddir.mkdir("Run summary")
    cddir.cd()

    for histo in filledHistograms:
      histo.Write()
    
    outputFile.Close()

def main(reffile, testfile, refdir, testdir):
    createHistograms(reffile, refdir)
    createHistograms(testfile, testdir)

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
