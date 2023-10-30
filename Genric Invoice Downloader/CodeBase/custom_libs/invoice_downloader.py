import requests
from datetime import datetime
import logging
import urllib.parse
import os


def extract_invoice_id(url,portal_name):
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    if portal_name == "RealPage":
        token_value = query_params[".token"][-1]
        segments = token_value.split('/')
        invoice_id = segments[-1]
        return invoice_id

    elif portal_name == "AvidSuite":
        url_parts = parsed_url.path.split("/")
        if url_parts:
            invoice_id = url_parts[-1]
            return invoice_id
        else:
            return None
    elif portal_name == "BankTel":
        if "invoiceId" in query_params:
            invoice_id = query_params["invoiceId"][0]
            return invoice_id
        else:
            return None

    else:
        return None
    


def invoiceDownload(url, save_directory, invoice_id,domain):
    try:
        parsed_url = urllib.parse.urlparse(url)  # Parse the URL
        logging.info(f"InvoiceDownloaderFunc: Invoice to download from URL: {url}")
        data = requests.get(url)
        logging.info("InvoiceDownloaderFunc: Successfully downloaded invoice from URL")

        today_date_time = datetime.now().strftime("%Y%m%d%H%M%S")

        if invoice_id:
            if domain == "RealPage":
                unique_filename = f"{parsed_url.netloc}_{today_date_time}_{invoice_id}.pdf"
            else:
                unique_filename = f"{parsed_url.netloc}_{today_date_time}.pdf"

            # Ensure the directory structure exists
            os.makedirs(save_directory, exist_ok=True)

            # Save the PDF file directly in the save_directory
            save_path = os.path.join(save_directory, unique_filename)

            # Log the save_path for debugging
            logging.info(f"Save path: {save_path}")

            with open(save_path, 'wb') as file:
                file.write(data.content)
            logging.info("InvoiceDownloaderFunc: Successfully downloaded invoice from URL")

            return save_path
        else:
            logging.warning("InvoiceDownloaderFunc: Invoice ID not found in the URL")
            return None
    except Exception as e:
        logging.exception("InvoiceDownloaderFunc: Error in downloading or saving the invoice")
        raise






