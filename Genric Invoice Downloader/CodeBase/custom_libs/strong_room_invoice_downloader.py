import requests
from bs4 import BeautifulSoup
import os

def download_iframe_content_from_file(html_file_path, invoice_id, strong_room_content_url, output_directory,AzADCookie):
    try:
        # Read the HTML source file
        with open(html_file_path, 'r', encoding='utf-8') as html_file:
            page_source = html_file.read()

        # Parse the HTML source to find the iframe_src dynamically
        soup = BeautifulSoup(page_source, 'html.parser')
        iframe = soup.find('iframe')

        if iframe:
            iframe_src = iframe['src']

            # Construct the complete URL by combining it with the base URL
            content_url = f"{strong_room_content_url}/{iframe_src}"
            payload = "__VIEWSTATE=%2FwEPDwUKMTcxMTMzNzc1OGRk1k%2BJcogVOAuKxguWb6rzJX3pkvVZVrVDQhXc%2FfphTqo%3D&__VIEWSTATEGENERATOR=4A2437CB"
            headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'en-US,en;q=0.5',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
    'Cookie': AzADCookie
}

            response = requests.post(content_url,headers=headers,data=payload)

            if response.status_code == 200:
                if response.headers.get('Content-Type') == 'application/pdf':
                    output_file_name = f"Strong_Room_Document_{invoice_id}.pdf"
                    output_file_path = os.path.join(output_directory, output_file_name)

                    with open(output_file_path, 'wb') as output_file:
                        output_file.write(response.content)
                    print(f"Content downloaded and saved to {output_file_path}")
                else:
                    print("Response is not a PDF.")
            else:
                print(f"Failed to download content from {content_url}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")