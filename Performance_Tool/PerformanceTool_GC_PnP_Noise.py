# -*- coding: utf-8 -*-


#Description : Website loading timing calculation tool for Google Chrome browser
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

from webdriver_manager.chrome import ChromeDriverManager


import json
#from browsermobproxy import Server

import time
import os


import random
from random import randrange
from requests.exceptions import HTTPError
import requests
from datetime import datetime, timedelta, date
import re
#import wget


import webbrowser



import sys

#Set the main working directory
os.chdir("/home/seonghun/Desktop/Seonghun/PerformanceTool")




#Create the webdriver object Options
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)


# Enable Performance Logging of Chrome.
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL","browser":"ALL"}


# Create the webdriver object and pass the arguments
# Chrome will start in Headless mode
#options.add_argument('headless')

# Ignores any certificate errors if there is any
#options.add_argument("--ignore-certificate-errors")

# Startup the chrome webdriver with executable path and
# pass the chrome options and desired capabilities as
# parameters.


#specify the path to chromedriver.exe (download and save on your computer)
s_gc=Service("/home/seonghun/Desktop/Seonghun/PerformanceTool/chromedriver")

#open driver and the webpage
driver = webdriver.Chrome(service=s_gc, options=chrome_options,desired_capabilities=desired_capabilities)

#driver = webdriver.Chrome(ChromeDriverManager().install())


web_apend = "https://"
web_add=sys.argv[1]
address = web_apend + web_add
#print(address)
full_address=str(address)
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

with open('LoadingTime_GC_PnP_noise.txt','a',encoding='utf-8') as f:
	f.write(str(loadingTime)+'\n')


print("Quitting WebDriver")
driver.quit()

