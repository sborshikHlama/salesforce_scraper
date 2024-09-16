"""
This module consists of fucntions for getting data fron NPS Overview report Medalia web page 
"""

from selenium.webdriver.common.by import By
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules.selenium_help_module import click_button, setup_driver

def download_nps(nps_url, username_nps, password_nps, nps_folder):
    """
    Setting up folder path for downloading data form nps report web page
    Params: nps_url, username_nps, password_nps, nps_folder, setup_driver
    """
    driver = setup_driver(nps_folder)
    # Remove previouse version of the file
    for file_name in os.listdir(nps_folder):
        file_path = os.path.join(nps_folder, file_name)
        try:
            # Check if it's not a Dashboard or Source file (we don't want to delete them)
            if os.path.isfile(file_path) and "NPS" in file_name:
                os.remove(file_path)
                print(f"Deleted old file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {str(e)}")
    # Run selenium script to scrap data from web page
    get_nps(nps_url, username_nps, password_nps, driver)
    while(len(os.listdir(nps_folder)) == 0):
        time.sleep(1)

def get_nps(url, username, password, driver):
    """
    Logging in when it's required and geting data from report.
    Params: url, username, password, driver
    """

    # Get list of open tabs
    initial_window_handles = driver.window_handles
    
    # For each file we open new tab (tab is called window in selenium)
    driver.execute_script("window.open('');")
    time.sleep(1)
    
    # Get list of open tabs once more to track new tabs 
    new_window_handles = driver.window_handles
    
    # Finding new window that has been open using initial_window_handles and new_window_handles
    new_window = [window for window in new_window_handles if window not in initial_window_handles][0]
    # Switching to new tab
    driver.switch_to.window(new_window)
    print(f"Switched to new window: {driver.current_window_handle}, URL: {driver.current_url}")
    
    # Open url from url list
    driver.get(url)
    time.sleep(5)

    # If its the first url form the list login is required
    try:
        # Get login input elements
        username_field = driver.find_element(By.NAME, 'loginfmt')
        username_field.send_keys(username)
        click_button(driver, By.ID, "idSIButton9")
        password_field = driver.find_element(By.NAME, 'passwd')
        password_field.send_keys(password)
        click_button(driver, By.ID, 'idSIButton9')
        click_button(driver, By.ID, 'idBtn_Back')
             
        # Waiting until page elements are loaded
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@class='sc-1a3m684-0 sc\
            -18q2bhg-0 kELszo bttVIH sc-lt20rn-2 hXuLgV']//div//*[name()='svg']")))
    
    except Exception:
        # If login elements not found, it means that login is not required
        print("Login not required, proceeding with the next step...")
    time.sleep(5)
    # Locate button and then click (if didn't work repeat one more time)
    click_button(driver, By.XPATH, "//button[@class='sc-1a3m684-0 sc-18q2bhg-0 kELszo bttVIH sc-lt20rn-2 hXuLgV']//\
        div//*[name()='svg']")

    click_button(driver, By.XPATH, "//button[normalize-space()='Excel']")