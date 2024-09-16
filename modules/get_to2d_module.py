"""
This module consitst of function for downloading TO2D from Celonis report web page
"""

from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
import os
from selenium.webdriver.remote.webdriver import WebDriver
from modules.selenium_help_module import click_button, setup_driver

def download_to2d(nps_url, username_nps, password_nps, download_folder)->None:
    """
    Deletes all old files from the
    folder. It connects chromedriver and sets up driver options,
    loops through the URLs list and calls get_data function
    Params: urls, username, password, download_folder, setup_driver
    """
    driver: WebDriver = setup_driver(download_folder)
    # Remove previouse files form folder
    for file_name in os.listdir(download_folder):
        file_path = os.path.join(download_folder, file_name)
        try:
            if os.path.isfile(file_path) and ("CELONIS" in file_name or "TO2D" in file_name):
                os.remove(file_path)
                print(f"Deleted old file: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {str(e)}")
    get_to2d(nps_url, username_nps, password_nps, driver)
    while(len(os.listdir(download_folder)) == 0):
        time.sleep(1)
    time.sleep(5)
    for file_name in os.listdir(download_folder):
        if ("CELONIS" in file_name):
            os.rename(os.path.join(download_folder, file_name), os.path.join(download_folder, "TO2D.xlsx"))
    time.sleep(10)
    driver.quit()

def get_to2d(url, username, password, driver: WebDriver):
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
    time.sleep(15)

    # If its the first url form the list login is required
    try:
        # Get login input elements
        username_field = driver.find_element(By.NAME, 'loginfmt')
        username_field.send_keys(username)
        click_button(driver, By.ID, 'idSIButton9')
        password_field = driver.find_element(By.NAME, 'passwd')
        # If elements are found login
        password_field.send_keys(password)
        click_button(driver, By.ID,'idSIButton9')
        click_button(driver, By.ID,'idBtn_Back')
    except Exception:
        # If login elements not found, it means that login is not required
        print("Login not required, proceeding with the next step...")

    # Get the current date
    current_date = datetime.now()

    # Calculate the first day of the current month
    first_day_of_current_month = current_date.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1).date().strftime("%Y-%m-%d")
    time.sleep(20)
    start_date = driver.find_element(By.XPATH, "//input[@aria-label='First Date']")
    start_date.clear()
    start_date.send_keys(first_day_of_previous_month)
    end_date = driver.find_element(By.XPATH, "//input[@aria-label='Last Date']")
    end_date.clear()
    end_date.send_keys(current_date.date().strftime("%Y-%m-%d"))
    # Export file
    time.sleep(10)
    click_button(driver, By.XPATH, "//div[@title='Fully Touchless Quarterly Evolution']")
    click_button(driver, By.XPATH, "//i[@title='Export']")
    click_button(driver, By.XPATH, "//a[normalize-space()='Export Cases (XLSX)']")