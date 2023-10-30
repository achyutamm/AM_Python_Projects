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


strong_room_url = "https://docview.payableslockbox.com/MyInvoices.aspx"
# strong_room_pdf_url = "https://docview.payableslockbox.com/docview/invoiceviewer.aspx?i=19061884&c=ASC_CLR&s=a01ddbdb-e209-f3ac-52f5-c6fca306d0ea"
strong_room_pdf_url = input("Enter the Strong Room URL")
s_username = "bpbot.serviceaccount"
z_pwd = "Applesauce1"
http_cookie_file_path = r'C:\Python\Genric Invoice Downloader\HTTP Cookie\HTTP Cookie.txt'
page_source_file_path  = "C:\\Python\\Genric Invoice Downloader\\Strong Room Page Source"
strong_room_content_url = "https://docview.payableslockbox.com/docview/"
document_output_path = "C:\\Python\\Genric Invoice Downloader\\Output\\"
strong_room_cookie_file_path = r'C:\Python\Genric Invoice Downloader\Strong Room HTTP Cookie\Strong Room HTTP Cookie.txt'






def write_cookies_to_file(cookies, filename):
    try:
        with open(filename, 'w') as file:
            for cookie in cookies:
                file.write(f'"{cookie["name"]}={cookie["value"]}"; ')
        print(f"Cookies written to {filename}")
    except Exception as e:
        print(f"Error writing cookies to file: {e}")

logging.basicConfig(level=logging.INFO)


def extract_id_from_url(url):
    try:
        url_parts = url.split('=')
        invoice_id = url_parts[1].split('&')[0]
        return invoice_id
    except:
        return None
    

def read_cookie_text_file(strong_room_cookie_file_path):
    try:
        with open(strong_room_cookie_file_path, 'r') as file:
            AzADCookie = file.read()
        return AzADCookie
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    




chrome_options = Options()
chrome_options.headless = False
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--incognito")
your_exec_path = "C:\\Python\\Genric Invoice Downloader\\Chrome Driver\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=your_exec_path, options=chrome_options)

driver.get(strong_room_url)
logging.info(f"Chrome driver has been started and loaded URL: {strong_room_url}")
time.sleep(6)
elements = driver.find_elements_by_css_selector("#UserName")
username = elements[0]
username.clear()
username.send_keys(s_username)
logging.info(f"User name has entered: {z_pwd}")
elements = driver.find_elements_by_css_selector("#Password")
password = elements[0]
password.clear()
password.send_keys(z_pwd)
logging.info(f"Password  has entered: {z_pwd}")


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
sec_text_box1.send_keys(z_pwd)
logging.info(f"Security Question 1 has entered : {z_pwd} answer")
sec_text_box2 = driver.find_element_by_id("IdentityVerification_IVerificationQandA_txtAnswer2")
sec_text_box2.send_keys(z_pwd)
logging.info(f"Security Question 2 has entered : {z_pwd} answer")
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


all_cookies = driver.execute_cdp_cmd("Network.getAllCookies", {})
# print(print(all_cookies))

# write_cookies_to_file(all_cookies,http_cookie_file_path)
# logging.info(f"HTTP cookies succesfully written in file at : {http_cookie_file_path}")

driver.get(strong_room_pdf_url)
time.sleep(8)



page_source = driver.page_source


invoice_id = extract_id_from_url(strong_room_pdf_url)
if invoice_id:
    html_file_path = f"{page_source_file_path}\\strong_room_page_source_{invoice_id}.html"
    with open(html_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(page_source)
else:
    print("Failed to extract the ID from the URL.")




logging.info(f"Driver has been succesfully closed")

AzADCookie = read_cookie_text_file(strong_room_cookie_file_path)
# AzADCookie = AzADCookie.encode('ascii', 'ignore').decode('ascii')
logging.info(f"Stron Room Portal HTTP Cookie: {str(AzADCookie)}")

# Download content from iframe using the module function
download_iframe_content_from_file(html_file_path, invoice_id, strong_room_content_url, document_output_path,AzADCookie)
driver.quit()