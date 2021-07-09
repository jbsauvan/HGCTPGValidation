#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys,subprocess
#python2
import urllib
import re

from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
argv.remove( '-b-' )

from ROOT import TCanvas
from graphFunctions import createWebPageLite, initRootStyle

sys.path.append('../')
for p in sys.path:
    print(p)

def createDir(webdir):
    os.system('mkdir ' + webdir)

def main(refdir, testdir, webdir):
    # graphical initialization
    initRootStyle()
    cnv = TCanvas("canvas")    
    
    createDir(webdir)
    createDir(webdir + '/img')
    
    # Files names
    filename = "/DQM_V0001_R000000001__validation__HGCAL__TPG.root"
    #  filename = "/DQM_V0001_new_R000000001.root"
    input_rel_file = refdir + filename
    input_ref_file = testdir + filename
    path_1 = 'DQMData/Run 1/HGCALTPG/Run summary'
    path_2 = path_1
    print('input_rel_file=', input_rel_file)
    print('input_ref_file=', input_ref_file)
    
    # web page creation. Title and others items are included into the createWebPage() function.
    createWebPageLite(input_rel_file, input_ref_file, path_1, path_2, cnv, webdir)

    print("Fin.")

if __name__=='__main__':
    import optparse
    import importlib
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--refdir', dest='refdir', help=' ', default='')
    parser.add_option('--testdir', dest='testdir', help=' ', default='')
    parser.add_option('--webdir', dest='webdir', help=' ', default='')
    (opt, args) = parser.parse_args()

    main(opt.refdir, opt.testdir, opt.webdir)
