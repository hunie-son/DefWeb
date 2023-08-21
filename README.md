# DefWeb: Defending User Privacy against Cache-based Website Fingerprinting Attacks with Intelligent Noise Injection
We develop a dynamic generative learning-based defense technique, DefWeb, to protect user privacy against cache-based Website Fingerprinting(WF) attacks by injecting precise noise into the WFs. For this purpose, (1) we train Variational Autoencoder (VAE) to represent high-dimensional fingerprints in a low-dimension space while creating distinct clusters for each website. (2) Minimal noise templates are extracted in the low-dimension space to obfuscate the fingerprints efficiently. (3) We create practical noise templates that can be added to WFs during website rendering by leveraging self-modifying code (SMC). We implement Def Web in simulation and real-world setups to degrade the attacker’s model accuracy. DefWeb can decrease the model accuracy to 1.1% and 28.8% in simulation and real-world setups, respectively.  

# Experimental Setup:
- ## Intel Tiger Lake Microarchitecture
  * CPU Model: Intel(R) Core (TM) i7-1165G7 @ 2.80GHz
  * OS: Ubuntu 20.04.4 LTS
  * Linux Kernel: 5.13.0-44-generic
  * Google Chrome version 101.0.4951.64
  * Tor browser version 10.5.10
- ## Additional 
  * Nvidia GeForce RTX 3090 GPU card
  * Software: MATLAB R2021


# Data Collection:
## Sweep-Counting (Cache-based WF attack)
## Loop-Counting (Interrupt based WF attack)

For collecting Website Fingerprints for different websites, follow the steps mentioned below:<br/>
- For the offline phase, the attacker can change the cache size in his device to match the victim's device and collect data which will be employed to train the ML model. 

- Data collection for Google Chrome Browser: We have collected 100 WF measurements for each of 100 different websites ([Website list]((https://github.com/website_list.txt)). We are going to record 100 individual measurements of 10 websites at a single run and save it in a single csv file. The `<name>.sh` is written to record data for the first 10 websites and will be saved in the `web1_10.csv` file. Similarly, the `<name>.sh` is responsible for collecting data for the next 10 websites and will be saved in `web11_20.csv` file. By following the commands mentioned below, five csv files will be created and saved in the directory, which we will call raw data. 

 - Preprocessing: We merge all the Collected csv files in one single file in name order.

- Data collection for Firefox Browser:
The procedure is the same for Firefox Browser as well. For the Firefox Browser scenario, follow the commands below: <br/>

  
- Preprocessing: For preprocessing the raw data, run the  [Data_process_tor.m](https://github.com/main/Data_Collection/Data_process%20_tor.m) file in Python,

After preprocessing the data, the final data for different devices are allocated to the appropriate folders.


# WF Attack:
### Instruction to run:
- Offline phase:


# DefWeb :
## Instruction to run:
## SMC generated precise noise Template:


# Performace Tool
## Instruction to run:

