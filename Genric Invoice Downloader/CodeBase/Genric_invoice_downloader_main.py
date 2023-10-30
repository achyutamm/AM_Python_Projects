import requests
import uuid
import os
from invoice_downloader import invoiceDownload, extract_invoice_id
import socket
import config_reader
import  os,platform,logging
from datetime import date
from datetime import datetime
from datetime import datetime, timedelta
import time
import urllib.parse


machine_name = socket.gethostname()
config_data = config_reader.load_config("C:\\Python\\Genric Invoice Downloader\Config\\appconfig.yaml")
environment = "Producution"


if environment == "Producution":
    invoice_output_path = config_data['production']['file_path']['invoice_output_path']
    log_file_path = config_data['production']['file_path']['log_file_path']
    chrome_driver_path = config_data['production']['file_path']['chrome_driver_path']


elif environment == "Development":

    invoice_output_path = config_data['production']['file_path']['invoice_output_path']
    log_file_path = config_data['production']['file_path']['log_file_path']




def log_file_setup():
    today = date.today()
    today_date_folder = today.strftime("%m%d%Y")
    timestr = time.strftime("%H%M")
    log_folder = log_file_path+today_date_folder+"/"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    return log_folder 


def get_domain_config(invoice_url, config):
    parsed_url = urllib.parse.urlparse(invoice_url)
    domain = parsed_url.netloc
    matched_portal = None
    for portal in config['production']['invoice_config']:
        if portal['domain'] == domain:
            matched_portal = portal
            break

    if matched_portal:
        portal_name = matched_portal['portal_name']
        download_url_pattern = matched_portal['download_url_pattern']

        invoice_download_url = download_url_pattern
        logging.info(f"Downloading invoice from {portal_name} - URL: {invoice_url}")
        # return extract_invoice_id(invoice_url), portal_name
        return portal_name
    else:
        logging.warning("Domain not found in the configuration. Unable to determine the portal.")
        return None, None





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
    logging_file=os.path.join(os.getenv('HOMEDRIVE'),os.getenv('HOMEPATH'),log_file_path+'Process_log.log')

   
    invoice_url = input("Enter the invoice URL: ")
    logging.info(f"Got {invoice_url} from Blue Prism")

    # call get_domain_config function for getting invoice portal name and domain from config file
    portal_name = get_domain_config(invoice_url, config_data)

    # Call extract_invoice_id function to get the invoice ID
    invoice_id = extract_invoice_id(invoice_url,portal_name)
    if invoice_id:
        logging.info(f"Extracted invoice ID: {invoice_id}")

    # Call invoiceDownload function to download and save the invoice
    result = invoiceDownload(invoice_url, invoice_output_path,invoice_id,portal_name)

    if result:
        logging.info(f"Invoice saved to: {result}")
 