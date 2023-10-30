from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import config_reader
import  os,platform,logging
import socket
from datetime import date
from datetime import datetime
from datetime import datetime, timedelta
import json
import requests
from bs4 import BeautifulSoup
from strong_room_invoice_downloader import download_iframe_content_from_file
import config_reader

machine_name = socket.gethostname()
config_data = config_reader.load_config("C:\\Python\\Genric Invoice Downloader\Config\\appconfig.yaml")
environment = "Producution"


if environment == "Producution":
    strrong_room_user_name = config_data['production']['strong_room_portal']['strrong_room_user_name']
    strrong_room_pwd = config_data['production']['strong_room_portal']['strrong_room_pwd']
    strrong_room_url = config_data['production']['strong_room_portal']['strrong_room_url']
    stron_room_cookie_file_path = config_data['production']['file_path']['stron_room_cookie_file_path']
    strong_room_cookie_log_file_path = config_data['production']['file_path']['strong_room_cookie_log_file_path']
    chrome_driver_path = config_data['production']['file_path']['chrome_driver_path']



elif environment == "Development":

    strrong_room_user_name = config_data['production']['strong_room_portal']['strrong_room_user_name']
    strrong_room_pwd = config_data['production']['strong_room_portal']['strrong_room_pwd']
    strrong_room_url = config_data['production']['strong_room_portal']['strrong_room_url']
    stron_room_cookie_file_path = config_data['production']['file_path']['stron_room_cookie_file_path']
    strong_room_cookie_log_file_path = config_data['production']['file_path']['strong_room_cookie_log_file_path']
    chrome_driver_path = config_data['production']['file_path']['chrome_driver_path']



def write_cookie_string_to_file(cookie_string, filename):
    with open(filename, 'w') as file:
        file.write(cookie_string)
    logging.info(f"Cookies written to {filename}")
    



def log_file_setup():
    today = date.today()
    today_date_folder = today.strftime("%m%d%Y")
    timestr = time.strftime("%H%M")
    log_folder = strong_room_cookie_log_file_path+today_date_folder+"/"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    return log_folder 




if __name__ == "__main__":

    log_folder = log_file_setup()
    # logging.basicConfig(level=logging.INFO)

    if platform.platform('windows'):
        logging_file=os.path.join(os.getenv('HOMEDRIVE'),os.getenv('HOMEPATH'),log_folder+'Process_log.log')
    else:
        logging_file = os.path.join(os.getenv('HOME'),log_folder+'Process_log.log')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s : %(levelname)s :%(message)s',
                        filename=logging_file,
                        filemode='a')

    logging.info("** Genric Invoice Downloader process started in "+machine_name+"** ")
    logging_file=os.path.join(os.getenv('HOMEDRIVE'),os.getenv('HOMEPATH'),strong_room_cookie_log_file_path+'Process_log.log')


    chrome_options = Options()
    chrome_options.headless = False
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--incognito")
    your_exec_path = chrome_driver_path
    driver = webdriver.Chrome(executable_path=your_exec_path, options=chrome_options)

    driver.get(strrong_room_url)
    logging.info(f"Chrome driver has been started and loaded URL: {strrong_room_url}")
    time.sleep(6)
    elements = driver.find_elements_by_css_selector("#UserName")
    username = elements[0]
    username.clear()
    username.send_keys(strrong_room_user_name)
    logging.info(f"User name has entered: {strrong_room_pwd}")
    elements = driver.find_elements_by_css_selector("#Password")
    password = elements[0]
    password.clear()
    password.send_keys(strrong_room_pwd)
    logging.info(f"Password  has entered: {strrong_room_pwd}")


    loginbutton = driver.find_element_by_xpath("//input[@id='LoginButton']")
    loginbutton.click()
    logging.info(f"Succesfully clicked on login button")

    time.sleep(6)

    okbutton = driver.find_element_by_xpath("//input[@id='ButtonOK']")
    okbutton.click()
    logging.info(f"Succesfully clicked on OK buttnon")

    time.sleep(2)
    radio_button = driver.find_element_by_id("IdentityVerification_IVerificationPrompt_rblSelVerify_0")
    radio_button.click()
    logging.info(f"Succesfully clicked on check box sec question 1")
    time.sleep(3)
    next_button = driver.find_element_by_id("IdentityVerification_ButtonNext")
    next_button.click()
    logging.info(f"Succesfully clicked on check Next button")
    time.sleep(3)
    sec_text_box1 = driver.find_element_by_id("IdentityVerification_IVerificationQandA_txtAnwser1")
    sec_text_box1.send_keys(strrong_room_pwd)
    logging.info(f"Security Question 1 has entered : {strrong_room_pwd} answer")
    sec_text_box2 = driver.find_element_by_id("IdentityVerification_IVerificationQandA_txtAnswer2")
    sec_text_box2.send_keys(strrong_room_pwd)
    logging.info(f"Security Question 2 has entered : {strrong_room_pwd} answer")
    time.sleep(1)
    next_button2 = driver.find_element_by_id("IdentityVerification_ButtonNext")
    next_button2.click()
    logging.info(f"Succesfully clicked on check Next button")
    time.sleep(2)
    radio_button1 = driver.find_element_by_id("IdentityVerification_IVerificationUnknownDevice_TrustedDeviceOptions_rblSelDevice_1")
    radio_button1.click()
    logging.info(f"Succesfully clicked on device information pop-up")
    time.sleep(1)
    next_button2 = driver.find_element_by_id("IdentityVerification_ButtonNext")
    next_button2.click()
    logging.info(f"Succesfully clicked on device information Next button")
    time.sleep(8)

    all_cookies = driver.get_cookies()
    cookies_dict = {}
    for cookie in all_cookies:
        cookies_dict[cookie['name']] = cookie['value']
    logging.info(f"Cookie dictonory has been fetched: : {cookies_dict}")


    cookie_string = ""
    for key, value in cookies_dict.items():
        cookie_string += f"{key}={value}; "

    cookie_string = cookie_string.rstrip("; ")

    print(cookie_string)
    logging.info(f"Strong room http cookie has fetched Cookie: : {cookie_string}")

    write_cookie_string_to_file(cookie_string,stron_room_cookie_file_path)
    driver.quit()
    logging.info(f"Chrome Driver has been succesfully closed")
