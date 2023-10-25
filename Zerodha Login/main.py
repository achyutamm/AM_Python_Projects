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
import tkinter as tk
import traceback


config_data = config_reader.load_config("C://Python//Zerodha Login//Config//appconfig.yaml")
machine_name = socket.gethostname()
environment = "Producution"
if environment == "Producution":
    z_username = config_data['production']['zerodha_login']['username']
    z_password = config_data['production']['zerodha_login']['password']
    zerodha_url = config_data['production']['zerodha_login']['zerodha_url']
    driver_path = config_data['production']['chrome_driver']['driver_path']
    http_cookie_file_path = config_data['production']['http_cookie']['file_path']
    log_file_path = config_data['production']['log_folder']['log_file_path']

elif environment == "Development":
    z_username = config_data['production']['zerodha_login']['username']
    z_password = config_data['production']['zerodha_login']['password']
    zerodha_url = config_data['production']['zerodha_login']['zerodha_url']
    driver_path = config_data['production']['chrome_driver']['driver_path']
    http_cookie_file_path = config_data['production']['http_cookie']['file_path']
    log_file_path = config_data['production']['log_folder']['log_file_path']



def log_file_setup():
    today = date.today()
    today_date_folder = today.strftime("%m%d%Y")
    timestr = time.strftime("%H%M")
    log_folder = log_file_path+today_date_folder+"/"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    return log_folder 

def show_error_popup(exception_info):
    error_popup = tk.Toplevel()
    error_popup.title("Error")
    error_popup.geometry("400x200")
    error_label = tk.Label(error_popup, text="An error occurred:")
    error_label.pack()
    error_text = tk.Text(error_popup, height=5, width=40)
    error_text.pack()
    error_text.insert("1.0", exception_info)
    close_button = tk.Button(error_popup, text="Close", command=error_popup.destroy)
    close_button.pack()


def write_cookies_to_file(cookies, filename):
    try:
        with open(filename, 'w') as file:
            file.write(cookies)
        print(f"Cookies written to {filename}")
    except Exception as e:
        print(f"Error writing cookies to file: {e}")


 # Process start from here
try:
    log_folder = log_file_setup()


    if platform.platform('windows'):
        logging_file=os.path.join(os.getenv('HOMEDRIVE'),os.getenv('HOMEPATH'),log_folder+'Process_log.log')
    else:
        logging_file = os.path.join(os.getenv('HOME'),log_folder+'Process_log.log')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s : %(levelname)s :%(message)s',
                        filename=logging_file,
                        filemode='a')

    logging.info("** Zerodha Login process started in "+machine_name+"** ")
    logging_file=os.path.join(os.getenv('HOMEDRIVE'),os.getenv('HOMEPATH'),log_file_path+'Process_log.log')




    chrome_options = Options()
    chrome_options.headless = False
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--incognito")
    your_exec_path = driver_path
    driver = webdriver.Chrome(executable_path=your_exec_path, options=chrome_options)

    driver.get(zerodha_url)
    logging.info(f"Chrome driver has been started and loaded URL: {zerodha_url}")
    time.sleep(6)
    elements = driver.find_elements_by_css_selector("#userid")
    username = elements[0]
    username.clear()
    username.send_keys(z_username)
    logging.info(f"User name has entered: {z_username}")
    elements = driver.find_elements_by_css_selector("#password")
    password = elements[0]
    password.clear()
    password.send_keys(z_password)
    logging.info(f"Password  has entered: {z_password}")


    sub_elements = driver.find_element_by_xpath("//button[@class='button-orange wide']")
    sub_elements.click()
    logging.info(f"Succesfully clicked on submit button for OTP")

    time.sleep(25)
    # sub_elements = driver.find_element_by_xpath("//button[@class='button-orange wide']")
    # sub_elements.click()


    pop_submit = driver.find_element_by_xpath("//button[@class='button button-blue']")
    pop_submit.click()
    logging.info(f"Landing page pop-up succesfully clicked")

    # After logging in, retrieve the HTTP cookies
    cookies = driver.get_cookies()
    print('Cookies:')
    for cookie in cookies:
        print(f'{cookie["name"]}: {cookie["value"]}')
        logging.info(f'Cookie Name: {cookie["name"]}, Cookie Value: {cookie["value"]}')

    write_cookies_to_file(cookies,http_cookie_file_path)
    logging.info(f"HTTP cookies succesfully written in file at : {http_cookie_file_path}")

    # Close the browser
    driver.quit()
    logging.info(f"Driver has been succesfully closed")
except Exception as e:
    error_name = type(e).__name()
    exception_info = traceback.format_exc()
    show_error_popup(exception_info)
    logging.error(f'Error Name: {exception_info}')
    logging.error(f'Error Name: {error_name}, Exception Info: {exception_info}')
    tk.mainloop()
    driver.quit()

