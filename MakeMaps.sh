#!/usr/bin/bash

cd /home/atalarczyk/osmapa-garmin

mv logs/OSMapaPL.log logs/OSMapaPL.log_OLD
python3 -u ProduceDistributionsPL.py > logs/OSMapaPL.log 2>&1

mv logs/OSMapaPLext.log logs/OSMapaPLext.log_OLD
python3 -u ProduceDistributionsPLext.py > logs/OSMapaPLext.log 2>&1

mv logs/UpdateWWW.log logs/UpdateWWW.log_OLD
python3 -u UpdateWebPage.py > logs/UpdateWWW.log 2>&1 
