#!/bin/bash

###
# Description :
# This code is for Automatically running our DefWeb with 10 iterations of time 
# Run DefWeb_VAE_Auto_GC.py to generate a Noisy WF dataset
# Run (1) ExtractCo3Noise_RetrainCNN_Auto.py extract and modify the only noise. (2) Add to original WF. (3) Retrain the attacker's CNN model
# Output : Accuracy
# Author : Seonghun Son (S.H, Son)
# Last updated: 8/24/23 
###

for ((j=1;j<=10;j++))
do
    echo "############ VAE train : $j ############"
    python DefWeb_VAE_Auto_GC.py
    if [ -d "__pycache__/" ] 
    then
    	rm -r __pycache__/	
    else
    	echo "Error: Directory /path/to/dir does not exists for __pycache__."
    fi
    echo "############ CNN re-train with Noise Co3 : $j ############"
    python ExtractCo3Noise_RetrainCNN_Auto.py
    rm -r Reconstructed_x_100_6000_100D_GC.csv NoisyDataset_x_100_6000_100D_GC.csv
done

