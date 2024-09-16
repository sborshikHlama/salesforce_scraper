"""
This module consists of functions for accessing web page elements with selenium functions
"""

import os
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def click_button(driver, by_method: str, path: str, timeout=20, flag=""):
    """
    Clicks the button
    Params: url, username, password, driver
    """
    for _ in range(2):
        try:
            button_div = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by_method, path))
            )
            button_div.click()
            return
        except Exception:
            print("The problem is with button: ", flag if flag else path)
            continue
    driver.quit()
    exit("Error exit")

def setup_driver(download_folder)->WebDriver:
    """
    Setup browser to download files and save them to specific folder
    Params: download_folder
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(script_dir, '../chromedriver.exe')

    # Set chrome options to download files to specific folder
    chrome_options = webdriver.ChromeOptions()
    chrome_prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    chrome_options.add_experimental_option("prefs", chrome_prefs)
    # This code makes browser to work at the background
    # To see browser just comment out code below 
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--silent")
    chrome_options.add_argument("--disable-logging")

    # Creating a service from selenium to set up chrome automation
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return (driver)