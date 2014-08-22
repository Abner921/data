#!/bin/sh
basepath=$(cd `dirname $0`; pwd -P)
cd $basepath
echo $basepath
mkdir -p log/`date +%Y-%m/%d`

#Keyword
echo "start ferch Keyword report"
echo "start ferch Keyword report" >> log/`date +%Y-%m/%d`/sem-baidu-Keyword.log
python ReportPipeline.py -r Keyword -d pc -u day >> log/`date +%Y-%m/%d`/sem-baidu-Keyword.log  2>&1
python ReportPipeline.py -r Keyword -d mobile -u day >> log/`date +%Y-%m/%d`/sem-baidu-Keyword.log  2>&1
echo "end ferch Keyword report" >> log/`date +%Y-%m/%d`/sem-baidu-Keyword.log

#Campaign
echo "start ferch Campaign report"
echo "start ferch Campaign report" >> log/`date +%Y-%m/%d`/sem-baidu-Campaign.log
python ReportPipeline.py -r Campaign -d pc -u hour >> log/`date +%Y-%m/%d`/sem-baidu-Campaign.log  2>&1
python ReportPipeline.py -r Campaign -d mobile -u hour >> log/`date +%Y-%m/%d`/sem-baidu-Campaign.log  2>&1
echo "end ferch Campaign report" >> log/`date +%Y-%m/%d`/sem-baidu-Campaign.log

#Region
echo "start ferch Region report"
echo "start ferch Region report" >> log/`date +%Y-%m/%d`/sem-baidu-Region.log
python ReportPipeline.py -r Region -d pc -u day >> log/`date +%Y-%m/%d`/sem-baidu-Region.log  2>&1
python ReportPipeline.py -r Region -d mobile -u day >> log/`date +%Y-%m/%d`/sem-baidu-Region.log  2>&1
echo "end ferch Region report" >> log/`date +%Y-%m/%d`/sem-baidu-Region.log



