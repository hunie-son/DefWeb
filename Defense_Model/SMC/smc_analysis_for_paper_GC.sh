#!/bin/bash


# Javascript Attack Code
web_file="prime_probe_smc_analysis.html"

# Repeat and Time delay values generated based on SMC look-up table
data="repeat_delay_template.csv"

# Repeat, iteration, and delay values are read from the csv file
arr_repeat=($(tail -n +1 $data | cut -d ',' -f1))
arr_time=($(tail -n +1 $data | cut -d ',' -f2))
iteration=$((${#arr_repeat[@]}))

# Attack code is started in the Google Chrome browser
google-chrome $web_file&

# 1 second sleep to wait for the browser to open
sleep 1s

# Iterated over the values in the csv file till all noise patterns are created
for ((j=0;j < $iteration;j++));
  do
      echo ${arr_repeat[j]} ${arr_time[j]} | taskset -c 0 ./prog_800 &
      echo ${arr_repeat[j]} ${arr_time[j]} | taskset -c 1 ./prog_800 &
      echo ${arr_repeat[j]} ${arr_time[j]} | taskset -c 2 ./prog_800 &
      echo ${arr_repeat[j]} ${arr_time[j]} | taskset -c 3 ./prog_800 
  done

sleep 10s
# Kill the Google Chrome browser
killall chrome
