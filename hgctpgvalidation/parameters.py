import os
import sys
import attr
from attr.validators import instance_of

# Default constants 
nbrOfEvents = 50

@attr.s  
class ConfigFileParameters():
    validationRef = attr.ib(validator=instance_of(bool), default=True)
    validationTest = attr.ib(validator=instance_of(bool), default=True)
    installStep = attr.ib(validator=instance_of(bool), default=True)
    compileStep = attr.ib(validator=instance_of(bool), default=True)
    simulationStep = attr.ib(validator=instance_of(bool), default=True)
    scramArch = attr.ib(validator=instance_of(str), default='slc6_amd64_gcc700')
    releaseRefName = attr.ib(validator=instance_of(str), default='CMSSW_10_4_0_pre4')
    releaseTestName = attr.ib(validator=instance_of(str), default='CMSSW_10_4_0_pre4')
    workingRefDir = attr.ib(validator=instance_of(str), default=str(releaseRefName) +'_HGCalTPGValidation_ref')
    workingTestDir = attr.ib(validator=instance_of(str), default=str(releaseRefName) +'_HGCalTPGValidation_test')
    remoteRefBranchName = attr.ib(validator=instance_of(str), default='hgc-tpg-devel-'+str(releaseRefName))
    remoteTestBranchName = attr.ib(validator=instance_of(str), default='hgc-tpg-devel-'+str(releaseRefName))
    localRefBranchName = attr.ib(validator=instance_of(str), default='HGCalTPGValidation_ref')
    localTestBranchName = attr.ib(validator=instance_of(str), default='HGCalTPGValidation_ref')
    remoteRef = attr.ib(validator=instance_of(str), default='PFCal-dev')
    remoteTest = attr.ib(validator=instance_of(str), default='PFCal-dev')
    numberOfEvents = attr.ib(validator=instance_of(int), default=nbrOfEvents)
    conditions = attr.ib(validator=instance_of(str), default='auto:phase2_realistic')
    beamspot = attr.ib(validator=instance_of(str), default='HLLHC14TeV')
    step = attr.ib(validator=instance_of(str), default='USER:Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation')
    geometryRef  = attr.ib(validator=instance_of(str), default='Extended2023D17')
    geometryTest  = attr.ib(validator=instance_of(str), default='Extended2023D17')
    eraRefName = attr.ib(validator=instance_of(str), default='Phase2')
    eraTestName = attr.ib(validator=instance_of(str), default='Phase2')
    procModifiers = attr.ib(validator=instance_of(str), default='')
    inputRefFileName = attr.ib(validator=instance_of(str), default='file:/afs/cern.ch/work/j/jsauvan/public/HGCAL/TestingRelVal/CMSSW_9_3_7/RelValSingleGammaPt35/GEN-SIM-DIGI-RAW/93X_upgrade2023_realistic_v5_2023D17noPU-v2/2661406C-972C-E811-9754-0025905A60DE.root')
    inputTestFileName = attr.ib(validator=instance_of(str), default='file:/afs/cern.ch/work/j/jsauvan/public/HGCAL/TestingRelVal/CMSSW_9_3_7/RelValSingleGammaPt35/GEN-SIM-DIGI-RAW/93X_upgrade2023_realistic_v5_2023D17noPU-v2/2661406C-972C-E811-9754-0025905A60DE.root')
    customiseRefFile = attr.ib(validator=instance_of(str), default='L1Trigger/L1THGCal/customClustering.custom_2dclustering_constrainedtopological')
    customiseTestFile = attr.ib(validator=instance_of(str), default='L1Trigger/L1THGCal/customClustering.custom_2dclustering_constrainedtopological')
    dropedBranches = attr.ib(validator=instance_of(str), default='"drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT","drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT","drop l1tEMTFHit2016s_simEmtfDigis__HLT","drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT","drop l1tEMTFTrack2016s_simEmtfDigis__HLT"')
    webDirPath = attr.ib(validator=instance_of(str), default='./HGCALTPG_Validation/GIFS')

    def installWorkingRefDir(self):
        command = 'export SCRAM_ARCH=' + self.scramArch + ';'
        command += 'echo $SCRAM_ARCH'  + ';' 
        command += 'scramv1 p -n ' + self.workingRefDir + ' CMSSW ' + self.releaseRefName + ';' 
        command += 'cd ' + self.workingRefDir + '/src;' 
        command += 'echo $PWD; '
        command += 'eval `scramv1 runtime -sh`;'
        command += 'git cms-merge-topic ' + self.remoteRef + ':' + self.remoteRefBranchName + ';'
        command += 'git checkout -b ' + self.localRefBranchName + ' ' + self.remoteRef + '/' + self.remoteRefBranchName + ';'
        return command
    
    def installWorkingTestDir(self):
        command = 'export SCRAM_ARCH=' + self.scramArch + ';'
        command += 'echo $SCRAM_ARCH'  + ';'
        command += 'scramv1 p -n ' + self.workingTestDir + ' CMSSW ' + self.releaseTestName + ';'
        command += 'cd ' + self.workingTestDir + '/src;'
        command += 'echo $PWD; '
        command += 'eval `scramv1 runtime -sh`;'
        command += 'git cms-merge-topic ' + self.remoteTest + ':' + self.remoteTestBranchName + ';'
        command += 'git checkout -b ' + self.localTestBranchName + ' ' + self.remoteTest + '/' + self.remoteTestBranchName + ';'
        return command

    def runCompileRefStep(self):
        command = 'export SCRAM_ARCH=' + self.scramArch + ';'
        command += 'cd ' + self.workingRefDir + '/src; eval `scramv1 runtime -sh`;'
        command += 'scram b -j4; ' + 'echo === End of compilation ===;' + 'echo $PWD;'
        return command

    def runCompileTestStep(self):
        command = 'export SCRAM_ARCH=' + self.scramArch + ';'
        command += 'cd ' + self.workingTestDir + '/src; eval `scramv1 runtime -sh`;'
        command += 'scram b -j4; ' + 'echo === End of compilation ===;' + 'echo $PWD;'
        return command

    def runSimulationRefStep(self):
        command =  'export SCRAM_ARCH=' + self.scramArch + ';'
        command += 'cd ' + self.workingRefDir + '/src; eval `scramv1 runtime -sh`;'
        command += 'cmsDriver.py hgcal_tpg_validation -n ' + str(self.numberOfEvents) + ' --mc  --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW --conditions ' + self.conditions + ' '
        command += '--beamspot ' + self.beamspot + ' ' + '--step ' + self.step + ' '
        command += '--geometry ' + self.geometryRef +  ' ' + '--era ' + self.eraRefName + ' ' 
        if self.procModifiers !='':
           command += '--procModifiers ' + self.procModifiers + ' '
        command += '--inputCommands "keep *",' + self.dropedBranches + ' '
        command += '--filein ' + self.inputRefFileName + ' '
        command += '--no_output ' + '--customise=' + self.customiseRefFile + ' '
        customize_commands = 'process.MessageLogger.files.out_ref = dict(); process.Timing = cms.Service(\'Timing\', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service(\'SimpleMemoryCheck\', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)'
        if 'L1THGCalUtilities/hgcalTriggerValidation_cff' in self.step:
            customize_commands += '; process.TFileService = cms.Service(\'TFileService\',fileName = cms.string(\'ntuple.root\'))'
        command += '--customise_commands "'+ customize_commands +'"' + ';'
        return command
   

    def runSimulationTestStep(self):
        command =  'export SCRAM_ARCH=' + self.scramArch + ';'
        command += 'cd ' + self.workingTestDir + '/src; eval `scramv1 runtime -sh`;'
        command += 'cmsDriver.py hgcal_tpg_validation -n ' + str(self.numberOfEvents) + ' --mc  --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW --conditions ' + self.conditions + ' '
        command += '--beamspot ' + self.beamspot + ' ' + '--step ' + self.step + ' '
        command += '--geometry ' + self.geometryTest +  ' ' + '--era ' + self.eraTestName + ' ' 
        if self.procModifiers !='':
           command += '--procModifiers ' + self.procModifiers + ' '
        command += '--inputCommands "keep *",' + self.dropedBranches + ' '
        command += '--filein ' + self.inputTestFileName + ' '
        command += '--no_output ' + '--customise=' + self.customiseTestFile + ' '
        customize_commands = 'process.MessageLogger.files.out_test = dict(); process.Timing = cms.Service(\'Timing\', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service(\'SimpleMemoryCheck\', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)'
        if 'L1THGCalUtilities/hgcalTriggerValidation_cff' in self.step:
            customize_commands += '; process.TFileService = cms.Service(\'TFileService\',fileName = cms.string(\'ntuple.root\'))'
        command += '--customise_commands "'+ customize_commands +'"' + ';'
        return command
