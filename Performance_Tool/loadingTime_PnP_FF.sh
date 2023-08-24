#!/bin/bash

###
# Description :
# This code is for Automatically running our Performance Tool (Mozila Firefox) with reading 100 websites (from website_list.txt)
# Run (1) prime_probe_Test.html to perform JavaScript-base Prime and Probe attack.
# (2) PerformanceTool_GC_PnP.py by inputing website address ("$line")
# (3) Close all taps
#
# Make sure chrome driver is properly installed while runing PerformanceTool_GC_PnP.py code
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
  
  # value m can be change
  for ((m=50;m<=52;m++))
  do
    #JavaScript Code with PNP attack (no website address is contain this code)
    web_file="prime_probe_Test.html"


    # echo  $webfile | ./python_code
    # Run PNP code with firfox browser
    firefox $web_file &
    
    # Run our Performance Tool python code
	python3 PerformanceTool_FF_PnP.py "$line"  
    
	wmctrl -c "Firefox" -x "Navigator.Firefox"&
	sleep 5s
	
  done
  killall firefox
  sleep 2s
done < website_list.txt
#COMMENTS
