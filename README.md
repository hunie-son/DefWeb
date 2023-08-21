# DefWeb: Defending User Privacy against Cache-based Website Fingerprinting Attacks with Intelligent Noise Injection
We develop a dynamic generative learning-based defense technique, DefWeb, to protect user privacy against cache-based Website Fingerprinting(WF) attacks by injecting precise noise into the WFs. For this purpose, (1) we train Variational Autoencoder(VAE) to represent high-dimensional fingerprints in a low-dimension space while creating distinct clusters for each website. (2) Minimal noise templates are extracted in the low-dimension space to obfuscate the fingerprints efficiently. (3) We create practical noise templates that can be added to WFs during website rendering by leveraging self-modifying code (SMC). We implement Def Web in simulation and real-world setups to degrade the attacker’s model accuracy. DefWeb can decrease the model accuracy to 1.1% and 28.8% in simulation and real-world setups, respectively.  

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
