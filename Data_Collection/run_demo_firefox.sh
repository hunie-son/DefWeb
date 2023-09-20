#!/bin/bash

#JavaScript code based on the Website List
for ((i=1;i<=100;i++))
do
    echo "Website: $j Mesurement: $i"
    #Run Browser(Mozilla Firefox) with JavaScript Code (amazon.com)
    #Change to "PrimeProbe_google.html" to achieve google.com WF data
    firefox PrimeProbe_amazon.html &
        
    # Based on the attack occurring in 30s
    sleep 35s
    killall firefox
    sleep 10s
done

for ((i=1;i<=100;i++))
do
    echo "Website: $j Mesurement: $i"
    #Run Browser(Mozilla Firefox) with JavaScript Code (amazon.com)
    #Change to "PrimeProbe_google.html" to achieve google.com WF data
    firefox PrimeProbe_google.html &
        
    # Based on the attack occurring in 30s
    sleep 35s
    killall firefox
    sleep 10s
done
