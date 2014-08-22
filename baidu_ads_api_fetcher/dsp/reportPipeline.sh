#!/bin/sh

basepath=$(cd `dirname $0`; pwd -P)
cd $basepath
echo $basepath
logpath=log/`date +%Y-%m/%d`
mkdir -p $logpath
set -e
#Keyword
echo "start fetch Keyword report"
filename=dsp-baidu-Keyword.log
echo "start fetch Keyword report" >> $logpath/$filename
python ReportPipeline.py -r Keyword  >> $logpath/$filename  2>&1
echo "end fetch Keyword report" >> $logpath/$filename

#Campaign
echo "start fetch Campaign report"
filename=dsp-baidu-Campaign.log
echo "start fetch Campaign report" >> $logpath/$filename
python ReportPipeline.py -r Campaign  >> $logpath/$filename  2>&1
echo "end fetch Campaign report" >> $logpath/$filename

#Region
echo "start fetch Region report"
filename=dsp-baidu-Region.log
echo "start fetch Region report" >> $logpath/$filename
python ReportPipeline.py -r Region >> $logpath/$filename  2>&1
echo "end fetch Region report" >> $logpath/$filename

#Industry
echo "start fetch Industry report"
filename=dsp-baidu-Industry.log
echo "start fetch Industry report" >> $logpath/$filename
python ReportPipeline.py -r Industry >> $logpath/$filename  2>&1
echo "end fetch Industry report" >> $logpath/$filename



