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
time.sleep(5)

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
with open('LoadingTime_FF_PnP_no22.txt', 'a', encoding = 'utf-8') as f:
	f.write(str(loadingTime)+'\n')

print("Quitting WebDriver")
driver.quit()

