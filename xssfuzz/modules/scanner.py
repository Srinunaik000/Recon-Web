import requests
from bs4 import BeautifulSoup
from .vulnerabilities.xss import xss_payloads  # Import default XSS payloads

class Scanner:
    def __init__(self, args):
        self.args = args
        self.urls = self.load_urls()

    def load_urls(self):
        # Load URLs from file or single URL
        urls = []
        if self.args.file:
            # Handle file input for URLs
            try:
                with open(self.args.file, 'r') as f:
                    urls = [url.strip() for url in f.readlines() if url.strip()]
            except FileNotFoundError:
                print(f"Error: File '{self.args.file}' not found.")
        if self.args.url:
            urls.append(self.args.url)
        return urls

    def check_reflection(self, url):
        headers_to_test = {
            'Referer': f'https://malicious.com/?payload={xss_payloads[0]}',
            'User-Agent': f'Mozilla/5.0 {xss_payloads[0]}',
            'X-Forwarded-For': f'127.0.0.1, {xss_payloads[0]}',
            'Cookie': f'sessionid=abc123; payload={xss_payloads[0]}',
            'X-Custom-Header': f'payload={xss_payloads[0]}'
        }

        try:
            # Replacing FUZZ in the URL with the test_word ONLY
            test_url = url.replace('FUZZ', 'test') if 'FUZZ' in url else url

            # Check if the URL is valid
            if not test_url.startswith(('http://', 'https://')):
                print(f"Skipping invalid URL: {test_url}")
                return

            response = requests.get(test_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            reflected_in_source = 'test' in response.text
            reflected_in_html = 'test' in soup.get_text()
            reflected_in_script = any('test' in script.string for script in soup.find_all('script') if script.string)

            if reflected_in_source or reflected_in_html or reflected_in_script:
                print(f"[+] 'test' is reflected at {url}")
            elif not self.args.show_positive:
                print(f"[-] 'test' is not reflected at {url}")

            if self.args.check_headers:
                for header_name, header_value in headers_to_test.items():
                    response_with_header = requests.get(url, headers={header_name: header_value})
                    if any(payload in response_with_header.text for payload in xss_payloads):
                        print(f"[+] One or more XSS payloads reflected in response when setting '{header_name}' header at {url}")
                    else:
                        if not self.args.show_positive:
                            print(f"[-] No XSS payloads reflected in response when setting '{header_name}' header at {url}")

        except requests.exceptions.RequestException as e:
            print(f"Error accessing {url}: {e}")

    def run(self):
        # Ensure there are URLs to test
        if not self.urls:
            print("Error: No URLs provided for testing.")
            return

        for url in self.urls:
            print(f"\nTesting URL: {url}")
            self.check_reflection(url)

