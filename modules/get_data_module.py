"""
This module consists of functions for downloading CXTickets, CSAT, AR data from salesforce report web pages
"""

from selenium.webdriver.common.by import By
import time
import os
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from modules.selenium_help_module import click_button, setup_driver

def is_any_tab_loading(driver):
    """
    Check if any tab is loading at
    the end of the program to quit browser only when 
    everything was downloaded.
    It takes driver as an argument to manipulate tabs
    """
    # Get list of open tabs
    all_tabs = driver.window_handles
    
    # Using loop to access each tab from list of tabs
    for tab in all_tabs:
        try:
            # Making browser to switch to tab
            driver.switch_to.window(tab)
            # Using tab tittle to check if its loading
            title = driver.title
            if "Loading" in title:
                return True
        except:
            # If we can't access tab it doesn't always mean that there is an error
            # It can happen when tab still exists in tab lists but was already closed after downloading
            print(f"Tab {tab} does not exist or cannot be switched to.")
    return False 

def download_files(urls, username, password, download_folder):
    """
    Delete all old files from the
    folder. It connects chromedriver and sets up driver options,
    loops through the URLs list and calls get_data function
    Params: urls, username, password, download_folder
    """
    driver = setup_driver(download_folder)
    # Deleting old files from the downloading folder
    for file_name in os.listdir(download_folder):
        file_path = os.path.join(download_folder, file_name)
        try:
            if os.path.isfile(file_path) and not ("Dashboard" in file_name or "Source" in file_name):
                os.remove(file_path)
                print(f"Deleted old file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {str(e)}")
    
    # Getting data form all urls from the list
    for url in urls:
        try:
            get_data(url, username, password, driver)
        except Exception:
            sys.exit("Error: failed to get data")
    
    # Checking if all downloads are finished
    while (is_any_tab_loading(driver)):
        print("I'm here")
        time.sleep(1)
    time.sleep(2)
    # Closing the browser
    time.sleep(10)
    driver.quit()

def get_data(url, username, password, driver):
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
    time.sleep(1)

    # If its the first url form the list login is required
    try:
        # Get login input elements
        username_field = driver.find_element(By.ID, 'username')
        password_field = driver.find_element(By.ID, 'password')
            
        # If elements are found login
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button = driver.find_element(By.ID, 'Login')
        login_button.click()
            
        # Waiting until page elements are loaded
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'expected_element_after_login')))
    
    except Exception:
        # If login elements not found, it means that login is not required
        print("Login not required, proceeding with the next step...")

    # Check if iframe html element is found
    iframe_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
    )

    # Switch context to iframe to access elements inside of it
    driver.switch_to.frame(iframe_element)

    click_button(driver, By.CLASS_NAME, 'slds-dropdown-trigger.slds-dropdown-trigger_click.slds-button_last')
    click_button(driver, By.XPATH, '//span[contains(text(), "Export")]')
    driver.switch_to.default_content()
    click_button(driver, By.XPATH, '//span[contains(text(), "Details Only")]')

    try:
        select_element = driver.find_element(By.CLASS_NAME, "slds-select")
        select = Select(select_element)
    except Exception:
        select_element = driver.find_element(By.CLASS_NAME, "slds-select")
        select = Select(select_element)

    # Choose select option
    select.select_by_value('xlsx')

    # Locate button and then click (if didn't work repeat one more time)
    click_button(driver, By.CLASS_NAME, "slds-button.slds-button_neutral.uiButton--default.uiButton--brand.uiButton")
    # try:
    #     download_button = driver.find_element(By.CLASS_NAME, "slds-button.slds-button_neutral\
    #         .uiButton--default.uiButton--brand.uiButton")
    #     download_button.click()
    # except Exception:
    #     download_button = driver.find_element(By.CLASS_NAME, "slds-button.slds-button_neutral\
    #         .uiButton--default.uiButton--brand.uiButton")
    #     download_button.click()

    # Wait files to be saved in downloading folder
    time.sleep(1)