#!/bin/bash
###
# Description :
# This code is for automatically running our Performance Tool (Mozila Firefox) with reading 100 websites (from website_list.txt) and Noise Template (data)
# Run (1) prime_probe_Test.html to perform JavaScript-base Prime and Probe attack.
# (2) Load Noise Template create by SMC (data)
# (3) PerformanceTool_FF_PnP_Noise.py by inputing website address ("$line")
# (4) Close all taps
#
# Make sure chrome driver is properly installed while runing PerformanceTool_FF_PnP_Noise.py code
#
# Input : website_list.txt
# Ouput : Loading Time
# Author : Seonghun Son (S.H, Son)
# Last updated: 8/24/23
###



i=1
while read line
do
  
 
  for ((m=50;m<=52;m++))
  do
    #web_file="prime_probe_web"$i".html"
    web_file="prime_probe_Test.html"


    data="Noise_Template_reapeat_sleep/repeat_sleep_second_try_"$i"_"$m".csv"
    arr_repeat=($(tail -n +1 $data | cut -d ',' -f1))
    arr_time=($(tail -n +1 $data | cut -d ',' -f2))
    #arr_label=($(tail -n +1 $data | cut -d ',' -f3))
    iteration=$((${#arr_repeat[@]}))
    echo "$i and $m"
    #echo "Iteration: $iteration"
    #echo ${arr_repeat[@]}
    #echo ${arr_time[@]}
    #sleep 1s
    #COMMENTS
    #start=$(date +%s)
    
	# echo  $webfile | ./python_code
    firefox $web_file &
    #killall prog_800
    python3 PerformanceTool_FF_PnP_Noise.py "$line" &
    sleep 3s
    #echo "heyy"
    start=$(date +%s)
    for ((j=0;j < 15;j++));
    do 
    #   if [ "${arr_label[j]}" == 100 ];
    #   then
           #echo $j
           #echo ${arr_repeat[j]}
           #echo "Sleep for smc100"
           #echo ${arr_time[j]}
           #echo 1 1 | taskset -c 0 ./prog_100 &
           #echo 1 1 | taskset -c 1 ./prog_100 &
           #echo 1 1 | taskset -c 2 ./prog_100 &
           #echo 1 1 | taskset -c 3 ./prog_100
    #       echo ${arr_repeat[j]} ${arr_time[j]} | taskset -c 0 ./prog_100 &
    #       echo ${arr_repeat[j]} ${arr_time[j]} | taskset -c 1 ./prog_100 &
    #       echo ${arr_repeat[j]} ${arr_time[j]} | taskset -c 2 ./prog_100 &
    #       echo ${arr_repeat[j]} ${arr_time[j]} | taskset -c 3 ./prog_100
    #       sleep 0.2s
           #sleep 1s
            #echo ${arr_label[j]}
    #     else
            #echo 3 3 | taskset -c 0 ./prog_800 &
            #echo 3 3 | taskset -c 1 ./prog_800 &
            #echo 3 3 | taskset -c 2 ./prog_800 &
            #echo 3 3 | taskset -c 3 ./prog_800
            #echo "Sleep for smc800"
        echo ${arr_repeat[j]} ${arr_time[j]} | taskset -c 0 ./prog_800 &
        echo ${arr_repeat[j]} ${arr_time[j]} | taskset -c 1 ./prog_800 &
        echo ${arr_repeat[j]} ${arr_time[j]} | taskset -c 2 ./prog_800 &
        echo ${arr_repeat[j]} ${arr_time[j]} | taskset -c 3 ./prog_800 
        #sleep 0.1s
            #echo ${arr_label[j]}
      #    fi
      done
      end=$(date +%s)
      dur=$((end-start))
      killall prog_800
      echo "Duration: $dur" 
      sleep 5s
	  #killall firefox
      #wmctrl -c firefox
	  wmctrl -c "Firefox" -x "Navigator.Firefox"
	  sleep 5s
	  echo -e '\n'
      #echo $j  
  done
  killall firefox
  #killall chrome
  sleep 5s
  ((i++))
  echo -e '\n'
done <website_list_no22.txt
#COMMENTS
