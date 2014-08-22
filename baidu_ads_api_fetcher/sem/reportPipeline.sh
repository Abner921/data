#!/bin/sh
set -e
basepath=$(cd `dirname $0`; pwd -P)
cd $basepath
echo $basepath
logpath=log/`date +%Y-%m/%d`
mkdir -p $logpath

#Keyword
echo "start ferch Keyword report"
filename=sem-baidu-Keyword.log
echo "start ferch Keyword report" >> $logpath/$filename
python ReportPipeline.py -r Keyword -d pc -u day >> $logpath/$filename  2>&1
python ReportPipeline.py -r Keyword -d mobile -u day >> $logpath/$filename  2>&1
echo "end ferch Keyword report" >> $logpath/$filename

#Campaign
echo "start ferch Campaign report"
filename=sem-baidu-Campaign.log
echo "start ferch Campaign report" >> $logpath/$filename
python ReportPipeline.py -r Campaign -d pc -u hour >> $logpath/$filename  2>&1
python ReportPipeline.py -r Campaign -d mobile -u hour >> $logpath/$filename  2>&1
echo "end ferch Campaign report" >> $logpath/$filename

#Region
echo "start ferch Region report"
filename=sem-baidu-Region.log
echo "start ferch Region report" >> $logpath/$filename
python ReportPipeline.py -r Region -d pc -u day >> $logpath/$filename  2>&1
python ReportPipeline.py -r Region -d mobile -u day >> $logpath/$filename  2>&1
echo "end ferch Region report" >> $logpath/$filename



