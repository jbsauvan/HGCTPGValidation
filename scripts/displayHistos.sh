#!/bin/bash

echo 'Run displayHistos.sh'
echo $#
echo $1
echo $2
echo $3
echo $simu_env

if [ $simu_env -eq 1 ]
then
    # Config at Cern
    echo 'Config at Cern'
    source /opt/rh/python27/enable
    source /cvmfs/sft.cern.ch/lcg/releases/gcc/4.9.3/x86_64-slc6-gcc49-opt/setup.sh
    source /cvmfs/sft.cern.ch/lcg/releases/ROOT/6.06.06-a2c9d/x86_64-slc6-gcc49-opt/bin/thisroot.sh
elif [ $simu_env -eq 2 ]
then
    # Config at LLR in sl6, switch to python2
    echo 'Config at LLR in sl6, switch to python2'
    source /usr/share/Modules/init/bash
    module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles
    module purge
    module load python/2.7.9
    source /opt/exp_soft/llr/root/v6.06.00-el6-gcc48/etc/init.sh
else [ $simu_env -eq 3 ]
    # Config at LLR in sl7, switch to python2
    echo 'Config at LLR in sl7, switch to python2'
    source /usr/share/Modules/init/bash
    module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
    module purge
    # module load python/2.7.9
    # source /opt/exp_soft/llr/root/v6.06.00-el6-gcc48/etc/init.sh
    source /opt/exp_soft/llr/root/v6.12.06-el7-gcc49/etc/init.sh
    echo 'Installed sl7 environment at LLR'
fi

echo 'The Python version was changed to '
python -V
echo 'The ROOT version is '
root-config --version

# Create histograms if ntuples have been produced
if [[ -f "$1/ntuple.root" ]] && [[ -f "$2/ntuple.root" ]]; then
    echo 'Producing histograms from ntuples'
    python ../HGCTPGValidation/hgctpgvalidation/histosFromNtuple.py --reffile ntuple.root --testfile ntuple.root --refdir $1 --testdir $2
fi
# Extract Time information for all modules
find . -name "out_ref.log" | xargs grep "TimeModule>" > TimingInfo_ref.txt
find . -name "out_test.log" | xargs grep "TimeModule>" > TimingInfo_test.txt
# Extract Memory Check information and global Time information
python ../HGCTPGValidation/hgctpgvalidation/display/extractTimeMemoryInfos.py --reffile out_ref.log --testfile out_test.log --refdir $1 --testdir $2
# Create histograms Time/event/producer from TimingInfo_.txt 
python ../HGCTPGValidation/hgctpgvalidation/display/timing.py --reffile TimingInfo_ref.txt --testfile TimingInfo_test.txt --refdir $1 --testdir $2
# Compare histograms for the two releases and create pages
python ../HGCTPGValidation/hgctpgvalidation/display/standAloneHGCALTPGhistosCompare.py --refdir $1 --testdir $2 --webdir $3
