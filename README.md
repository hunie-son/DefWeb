# DefWeb: Defending User Privacy against Cache-based Website Fingerprinting Attacks with Intelligent Noise Injection
We develop a dynamic generative learning-based defense technique, DefWeb, to protect user privacy against cache-based Website Fingerprinting(WF) attacks by injecting precise noise into the WFs. For this purpose, (1) we train a Variational Autoencoder (VAE) to represent high-dimensional fingerprints in a low-dimension space while creating distinct clusters for each website. (2) Minimal noise templates are extracted in the low-dimension space to obfuscate the fingerprints efficiently. (3) We create practical noise templates that can be added to WFs during website rendering by leveraging self-modifying code (SMC). We implement Def Web in simulation and real-world setups to degrade the attacker’s model accuracy. DefWeb can decrease the model accuracy to 1.1% and 28.8% in simulation and real-world setups, respectively.  

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
## Cache-based WF attack (Robust Website Fingerprinting Through the Cache Occupancy Channel)
<!---- For collecting Website Fingerprints for different websites, follow the steps mentioned below:<br/>
  * For the offline phase, the attacker can change the cache size in his device to match the victim's device and collect data, which will be employed to train the ML model. 
  -->

- Data collection for Google Chrome Browser:
  * We have collected 100 WF measurements for each of 100 different websites [Website list](https://github.com/hunie-son/DefWeb/blob/main/Data_Collection/website_list.txt).
  * For the Demo, we are only using `PrimeProbe_Test_1.html` and `PrimeProbe_Test_2.html`, which is www.google.com and www.amazon.com, respectively. (You can create 100 different Prime and Probe attack JavaScript code based on the [Website list](https://github.com/hunie-son/DefWeb/blob/main/Data_Collection/website_list.txt))
  * Collecting WF dataset automatically using bash script <br/>
  `cd DefWeb/Data_Collection/Chrome`<br/>
  `./run_chrome.sh`<br/>
   * Collected 100 websites WF datasets are provided `DefWeb/Data_Collection/Chrome/Chrome_Collected_100`

- Data collection for Firefox Browser:
  * The procedure is the same as Chrome Browser. For the Firefox Browser scenario, follow the commands below: <br/>
   * Collecting WF dataset automatically using bash script <br/>
  `cd DefWeb/Data_Collection/Firefox`<br/>
  `./run_firefox.sh`<br/>
   * Collected 100 websites WF datasets are provided `DefWeb/Data_Collection/Firefox/Firefox_Collected_100`


- Preprocessing: For preprocessing the raw data, run the  [Data_process_tor.m](https://github.com/main/Data_Collection/Data_process%20_tor.m) file in Python,

After preprocessing the data, the final data for different devices are allocated to the appropriate folders.


# WF Attack:
- Preprocessing: We merge all the Collected csv files in one single file in name order.
### Instruction to run:
- Offline phase: CNN


# DefWeb :
## Instruction to run:
- Offline phase: VAE with two cluster->  
- Figure Google -> Amazone figure

## SMC generated precise noise Template:


# Performace Tool
## Instruction to run:

