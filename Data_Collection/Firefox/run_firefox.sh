#!/bin/bash

#Java Script code based on the Website List
for ((j=1;j<=100;j++))
do
    echo "Start Collecting Website $j"
    # Measurement for Collecting Dataset
    for ((i=1;i<=100;i++))
    do
        echo "Website: $j Mesurement: $i"
        firefox PrimeProbe_Test_"$j".html &
        #base on the attack occurs 30s
        sleep 35s
        killall firefox
        sleep 10s
    done
    echo "Done Collecting Website $j"
    
done


