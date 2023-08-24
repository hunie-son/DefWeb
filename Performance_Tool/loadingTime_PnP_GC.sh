#!/bin/bash

###
# Description :
# This code is for Automatically running our Performance Tool (Google Chrome) with reading 100 websites (from website_list.txt)
# Run (1) prime_probe_Test.html to perform JavaScript-base Prime and Probe attacks.
# (2) PerformanceTool_GC_PnP.py by inputting website address ("$line")
# (3) Close all taps
#
# Make sure the chrome driver is properly installed while running the PerformanceTool_GC_PnP.py code
#
# Input : website_list.txt
# Ouput : Loading Time
# Author : Seonghun Son (S.H, Son)
# Last updated: 8/24/23
###


#file = 'website_list.txt'


while read line
do
#for((i=1;i<=10;i++))
#do

  for ((m=50;m<=52;m++))
  # value m can be changed
  do
  #JavaScript Code with PNP attack (no website address contains this code)
  	web_file="prime_probe_Test.html"


    	# echo  $webfile | ./python_code
    	# Run PNP code with Chrome browser
   	google-chrome $web_file & 


    	# Run our Performance Tool Python code
    	python3 PerformanceTool_GC_PnP.py "$line"
    
	wmctrl -c "Google Chrome"&
	sleep 5s
	#killall google-chrome 
  done
  killall google-chrome
  sleep 2s
done < website_list.txt
