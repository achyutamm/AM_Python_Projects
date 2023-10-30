http_cookie_file_path = r"C:\Python\Sel_login\HTTP Cookie\HTTP Cookie.txt"

cookies = '''Cookies:
enctoken: iPGrOViVk7WhKb83S+n1KuG8+OGYWyetbirKRi+xbEBRKvGPBym7epTU4kxM2y1r9cywu6XiQKDWnzwuxfwxZx9bas54iVpkG5HzK6o5R/dqHGnogJiS2A=='''

def write_cookies_to_file(cookies, filename):
    try:
        with open(filename, 'w') as file:
            file.write(cookies)
        print(f"Cookies written to {filename}")
    except Exception as e:
        print(f"Error writing cookies to file: {e}")

write_cookies_to_file(cookies, http_cookie_file_path)
