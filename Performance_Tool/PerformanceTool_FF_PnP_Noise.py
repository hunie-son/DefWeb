# -*- coding: utf-8 -*-



#Description : Website loading timing calculation tool for Firefox browser
#Last Update : Jan.2.2023 (S.H)


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


#Firefox selenium option
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager


import json


import time
import os

import random
from random import randrange
from requests.exceptions import HTTPError
import requests
from datetime import datetime, timedelta, date
import re
#import wget


import sys


#Set the main working directory
os.chdir("/home/seonghun/Desktop/Seonghun/PerformanceTool")



# Enable Performance Logging of FIREFOX.
desired_capabilities = DesiredCapabilities.FIREFOX
desired_capabilities["loggingPrefs"] = {"Performaces": "ALL"}



# Create the webdriver object and pass the arguments
# Firefox will start in Headless mode

options = FirefoxOptions()
#options.add_argument("headless")


# Ignores any certificate errors if there is any
options.add_argument("--ignore-certificate-errors")


#driver = webdriver.Chrome(executable_path="C:/chromedriver.exe",chrome_options=options,desired_capabilities=desired_capabilities)

#specify the path to geckodriver (Firefox webdriver)
#s=Service("/Users/seonghun/Desktop/WebCroll/chromedriver")

#s_gc=Service("/home/gulmezoglu/Profiler/chromedriver")
s_ff=Service("/home/seonghun/Desktop/Seonghun/PerformanceTool/geckodriver")


#open driver and the webpage

driver = webdriver.Firefox(service=s_ff,options=options,desired_capabilities=desired_capabilities)
#driver = webdriver.Firefox(GeckoDriverManager().install())



web_a = "http://"
web_add = sys.argv[1]
address =web_a + web_add
full_address = str(address) 
driver.get(full_address)



#Time to set (second)
time.sleep(10)

navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
responseStart = driver.execute_script("return window.performance.timing.responseStart")
domComplete = driver.execute_script("return window.performance.timing.domComplete")
loadEventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")

# Calculate the performance
backendPerformance_calc = responseStart - navigationStart
frontendPerformance_calc = domComplete - responseStart
print("--------------------")

print("Back End time(ms): %s" % backendPerformance_calc)
print("Front End time(ms): %s" % frontendPerformance_calc)

total =  backendPerformance_calc + frontendPerformance_calc
print("Total time(ms): %s" % total)
print("--------------------")

loadingTime = loadEventEnd - navigationStart
print("Loading time(ms): %s" % loadingTime)
print("--------------------")
with open('LoadingTime_FF_PnP_noise.txt','a',encoding='utf-8') as f:
	f.write(str(loadingTime)+'\n')

print("Quitting WebDriver")
driver.quit()











# Tested Code with Porxy server to get the network log as JSON file format
'''
# Gets all the logs from performance in Chrome
logs = driver.get_log('Performaces')
print(logs)

# Opens a writable JSON file and writes the logs in it
with open("network_log_amazon.json", "w", encoding="utf-8") as f:
    f.write("[")

    # Iterates every logs and parses it using JSON

    for log in logs:
        network_log = json.loads(log["message"])["message"]

        # Checks if the current 'method' key has any
        # Network related value.

        if("Network.response" in network_log["method"]
                    or "Network.request" in network_log["method"]
                    or "Network.webSocket" in network_log["method"]):

            # Writes the network log to a JSON file by
            # converting the dictionary to a JSON string
            # using json.dumps().

            f.write(json.dumps(network_log)+",")
    f.write("{}]")

print("Quitting Selenium WebDriver")
driver.quit()

# Read the JSON File and parse it using
# json.loads() to find the urls containing images.
json_file_path = "network_log_amazon.json"
with open(json_file_path, "r", encoding="utf-8") as f:
    logs = json.loads(f.read())

# Iterate the logs

for log in logs:


# Except block will be accessed if any of the
# following keys are missing.

    try:
        # URL is present inside the following keys
        url = log["params"]["request"]["url"]

        # Checks if the extension is .png or .jpg
        if url[len(url)-4:] == ".png" or url[len(url)-4:] == ".jpg":
            print(url, end='\n\n')

    except Exception as e:
        pass


'''
