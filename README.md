# DefWeb: Defending User Privacy against Cache-based Website Fingerprinting Attacks with Intelligent Noise Injection
We develop a generative learning-based defense technique, DefWeb, to protect user privacy against cache-based Website Fingerprinting(WF) attacks by injecting precise noise into the WFs. For this purpose, (1) we train a Variational Autoencoder (VAE) to represent high-dimensional fingerprints in a low-dimension space while creating distinct clusters for each website. (2) Minimal noise templates are extracted in the low-dimension space to obfuscate the fingerprints efficiently. (3) We create practical noise templates that can be added to WFs during website rendering by leveraging self-modifying code (SMC). We implement DefWeb in simulation and real-world setups to degrade the attacker’s model accuracy. DefWeb can decrease the model accuracy to 1.1% and 28.8% in simulation and real-world setups, respectively.  

# Experimental Setup:
- ## Intel Tiger Lake Microarchitecture
  * CPU Model: Intel(R) Core (TM) i7-1165G7 @ 2.80GHz
  * OS: Ubuntu 20.04.4 LTS
  * Linux Kernel: 5.13.0-44-generic
  * Google Chrome version 101.0.4951.64
  * Tor browser version 10.5.10
    
- ## Deep Learning environment
  * Nvidia GeForce RTX 3090 GPU card
  * Jupyter Notebook (or Google Colab)
    
- ## Additional
  * Software: MATLAB R2021

# Enviroment explanations:
- ## Data Collection
  * This process should be done in the specific microarchitecture (In our case, we use Intel TigerLake).
  * We provide Chrome browser and Firefox collection code.
  * 
  * Approximate time: 1.3 hours for each website 

- ## CNN, LSTM and VAE model training
  * We train our models in a server environment (Nvidia GeForce RTX 3090 GPU card).
  * We use Jupyter Notebook(.ipynb) for the Demo version.
  * If GPU is unavailable, Google Colab can be used for running the Demo version.
  * Full version with 100 websites is provided as Python code (.py).
  * Automatically training 100 website fingerprinting is provided as bash script code (`DefWeb_Autorun.sh`).
  * At least 6GB of disk memory space is needed to save all the datasets (WF datasets, Reconstructed datasets, Noisy datasets, and pre-trained models)
  * Approximate time: more than 3-5 hours (depending on the GPU performance)
  


# Data Collection:
## Cache-based WF attack 
<!---- (Robust Website Fingerprinting Through the Cache Occupancy Channel)
   For collecting Website Fingerprints for different websites, follow the steps mentioned below:<br/>
  * For the offline phase, the attacker can change the cache size in his device to match the victim's device and collect data, which will be employed to train the ML model. 
  -->
- (Demo) With two Website Fingerprint (WF) datasets, which are www.google.com and www.amazon.com.
- In our project, we collected 100 measurements for each of 100 different websites [Website list](https://github.com/hunie-son/DefWeb/blob/main/Data_Collection/website_list.txt), overall 10,000 measurements.
  
- Data collection for Google Chrome Browser:
  * (Demo) `PrimeProbe_google.html` and `PrimeProbe_amazon.html` are JavaScript codes of Prime and Probe attack created by Dr. Yossi Oren's research team. (You can create 100 different Prime and Probe attack JavaScript codes based on the [Website list](https://github.com/hunie-son/DefWeb/blob/main/Data_Collection/website_list.txt))
    
  * (Demo) Collecting WF dataset 2 websites (www.amazon.com and www.google.com) automatically using bash script  <br/>
  `cd DefWeb/Data_Collection`<br/>
  `./run_demo_chrome.sh`<br/>
  
  * Collecting WF dataset 100 websites automatically using bash script (Chrome) <br/>
  `cd DefWeb/Data_Collection/Chrome`<br/>
  `./run_chrome.sh`<br/>
  
   * Collected 100 websites WF datasets are provided `DefWeb/Data_Collection/Chrome/Chrome_Collected_100`

- Data collection for Mozilla Firefox Browser:
  * (Demo) Collecting WF dataset 2 websites (www.amazon.com and www.google.com) automatically using bash script  <br/>
  `cd DefWeb/Data_Collection`<br/>
  `./run_demo_firefox.sh`<br/>
  
  * The procedure is the same as Chrome Browser [Website list](https://github.com/hunie-son/DefWeb/blob/main/Data_Collection/website_list.txt). <br/>
  
   * Collecting WF dataset 100 websites automatically using bash script (Firefox) <br/>
  `cd DefWeb/Data_Collection/Firefox`<br/>
  `./run_firefox.sh`<br/>
   * Collected 100 websites WF datasets are provided `DefWeb/Data_Collection/Firefox/Firefox_Collected_100`

- Preprocessing:
  * Merged CSV file (10,000 x 6,000) is large to upload in the GitHub repository.
    
  * We provide preprocessing python code ([Preprocessing_WF.ipynb](https://github.com/hunie-son/DefWeb/blob/main/Data_Collection/Preprocessing_WF.ipynb)) to create WF Dataset (single csv file) with the order.
    
  * (Demo) `trainX_2_US_Chrome.csv` and `trainY_2_US_Chrome.csv` are preprocessed WF dataset for wwww.amazon.com and www.google.com. 

After preprocessing the data, the final training data (trainX and trainY) will created.


# WF Attack:
- We use Convolutional Neural Networks (CNN) and Long Short-Term Memory Networks (LSTM) to conduct WF attacks.
   * We provide CNN python code ([CNN_Final.ipynb](https://github.com/hunie-son/DefWeb/blob/main/Attack_Model/CNN_Final.ipynb)) with explanation.
     
   * We provide LSTM python code ([LSTM_Final.ipynb](https://github.com/hunie-son/DefWeb/blob/main/Attack_Model/LSTM_Final.ipynb)) with explanation.
     
   * (Demo) Input data: Preprocessed data (`trainX_2_US_Chrome.csv` and `trainY_2_US_Chrome.csv`)
     
   * Output: Accuracy
  
<!----
### Instruction to run:
- Offline phase: CNN
-->

# DefWeb :
- VAE: We use a Generative Deep Learning Model, Variational AutoEncoder(VAE), to create dynamic noise.
  * (Demo) [DefWeb_VAE_Demo.ipynb](https://github.com/hunie-son/DefWeb/blob/main/Defense_Model/VAE/DefWeb_VAE_Demo.ipynb) contains detailed explanations (Approximate time: ~10min).
  * (Demo) Input data: Preprocessed data (`trainX_2_US_Chrome.csv` and `trainY_2_US_Chrome.csv`)
  * (Demo) Output data: Reconstructed data (`reconstructed_x_chrome_w2.csv`), Noisy Reconstructed data (`reconstructed_nosiy_x_chrome_w2.csv`)
    
  * `DefWeb_VAE_Auto_GC.py`:  Perform VAE and reconstruct the Noisy WF dataset (100 websites) 
  * `ExtractCo3Noise_RetrainCNN_Auto.py` : Extract 1/3 of noise. Add dynamic noise to the original WF dataset and retrain the attacker's CNN model.
  * Automatically execute DefWeb using bash script  <br/>
  `cd DefWeb/Defense_Model/VAE`<br/>
  `./DefWeb_Autorun.sh`<br/> 
   
    
- SMC: We use a Self-modifying Code (SMC) to generate practical noise template creation.
  * `noise_template.csv`: An example noise template generated by VAE. This is an analytical noise template that we need to mimic.
    
  * `repeat_delay_template.csv`: This file consists of repeat and delay values that will create a specific SMC practical noise.
    
  * `smc_example.csv`: An example SMC practical noise collected with the practical noise generation tool.
    
  * `prime_probe_smc_analysis.html`: Prime and Probe attack code to be run in a browser. This file was created by Dr. Yossi Oren's team.
    
  * `smc_analysis_for_paper_GC.sh`: This code runs the practical noise code. You are expected to run this code.
    
  * `SMC_generation_visualization_artifact_code.m`: The Matlab code to visualize both analytical and practical noise templates.
    
  * `smc.asm`: This code creates practical noise with given repeat and delay values.
    
  * `main.c`: This is the `main` code that runs the assembly file to create smc noise.
    
<!----

-->
# Noise Template
- Noise template datasets generated by DefWeb are provided for future research.
    
# Noise Template Repeat and Sleep
- Precise noise is created with SMC based on the repeat and sleep datasets.
- This is used for Performance Tool (Chrome browser with PnP attack + Noise)
  
# Performance Tool
- In this part, we automatically render(using Python library) the target website with Prime and Probe attack (JavaScript file location) and calculate the webpage loading time.
- Prerequisites: Chrome driver and Firefox driver need to be installed.
- We also perform website loading time with our DefWeb create noise template running.
  * Automatically execute Performance Tool (Chrome browser with PnP attack) using bash script <br/>
  `cd DefWeb/Performance_Tool`<br/>
  `./loadingTime_PnP_GC.sh`<br/>
  
  * Automatically execute Performance Tool (Mozilla Firefox with PnP attack) using bash script <br/>
  `cd DefWeb/Performance_Tool`<br/>
  `./loadingTime_PnP_FF.sh`<br/>
  
  * Automatically execute Performance Tool (Chrome browser with PnP attack + Noise) using bash script <br/>
  `cd DefWeb/Performance_Tool`<br/>
  `./loadingTime_PnP_noise_GC.sh.sh`<br/>
  
  * Automatically execute Performance Tool (Mozilla Firefox with PnP attack + Noise) using bash script <br/>
  `cd DefWeb/Performance_Tool`<br/>
  `./loadingTime_PnP_noise_FF.sh.sh`<br/> 


  
<!---- 
## Instruction to run:
-->
