#!/bin/bash

#JavaScript code based on the Website List
for ((i=1;i<=100;i++))
do
    echo "Website: $j Mesurement: $i"
    #Run Browser(Google Chrome) with JavaScript Code (amazon.com)
    #Change to "PrimeProbe_google.html" to achieve google.com WF data
    google-chrome PrimeProbe_amazon.html &
        
    #base on the attack occurs 30s
    sleep 35s
    killall chrome
    sleep 10s
done

for ((i=1;i<=100;i++))
do
    echo "Website: $j Mesurement: $i"
    #Run Browser(Google Chrome) with JavaScript Code (amazon.com)
    #Change to "PrimeProbe_google.html" to achieve google.com WF data
    google-chrome PrimeProbe_google.html &
        
    #base on the attack occurs 30s
    sleep 35s
    killall chrome
    sleep 10s
done
