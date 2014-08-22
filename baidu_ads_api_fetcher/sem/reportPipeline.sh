#!/bin/sh

basepath=$(cd `dirname $0`; pwd -P)
cd $basepath
echo $basepath
logpath=log/`date +%Y-%m/%d`
mkdir -p $logpath
set -e
#Keyword
echo "start fetch Keyword report"
filename=sem-baidu-Keyword.log
echo "start fetch Keyword report" >> $logpath/$filename
python ReportPipeline.py -r Keyword -d pc -u day >> $logpath/$filename  2>&1
python ReportPipeline.py -r Keyword -d mobile -u day >> $logpath/$filename  2>&1
echo "end fetch Keyword report" >> $logpath/$filename

#Campaign
echo "start fetch Campaign report"
filename=sem-baidu-Campaign.log
echo "start fetch Campaign report" >> $logpath/$filename
python ReportPipeline.py -r Campaign -d pc -u hour >> $logpath/$filename  2>&1
python ReportPipeline.py -r Campaign -d mobile -u hour >> $logpath/$filename  2>&1
echo "end fetch Campaign report" >> $logpath/$filename

#Region
echo "start fetch Region report"
filename=sem-baidu-Region.log
echo "start fetch Region report" >> $logpath/$filename
python ReportPipeline.py -r Region -d pc -u day >> $logpath/$filename  2>&1
python ReportPipeline.py -r Region -d mobile -u day >> $logpath/$filename  2>&1
echo "end fetch Region report" >> $logpath/$filename



