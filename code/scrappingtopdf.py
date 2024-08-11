import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from urllib.parse import urljoin
import time

# Base URL of the website
base_url = "https://vcet.edu.in/"

# Custom headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Function to get all internal links from the base URL
def get_internal_links(soup, base_url):
    links = set()
    for anchor in soup.find_all('a', href=True):
        link = anchor['href']
        if link.startswith('/'):
            link = urljoin(base_url, link)
        if base_url in link:
            links.add(link)
    return links

# Function to scrape content from a URL
def scrape_content(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            content = [tag.get_text(strip=True) for tag in soup.find_all(['h1', 'h2', 'h3', 'p'])]
            print(f"Scraped {len(content)} items from {url}")
            return content
        else:
            print(f"Failed to retrieve content from {url}, status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error while scraping {url}: {e}")
        return []

# Define a PDF class with customized header and footer
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Scraped Data', 0, 1, 'C')
        self.ln(10)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        try:
            body_encoded = body.encode('latin-1', 'replace').decode('latin-1')
        except UnicodeEncodeError:
            body_encoded = body.encode('utf-8', 'replace').decode('utf-8')
        self.multi_cell(0, 10, body_encoded)
        self.ln()

# Function to generate PDF from scraped data
def generate_pdf(data, filename):
    if not data:
        print(f"No data to write for {filename}. Skipping PDF generation.")
        return

    try:
        pdf = PDF()
        pdf.add_page()
        for item in data:
            pdf.chapter_body(item)
        pdf.output(filename)
        print(f"PDF generated: {filename}")
    except Exception as e:
        print(f"Error generating PDF {filename}: {e}")

# Main scraping and PDF generation process
def main():
    try:
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            main_soup = BeautifulSoup(response.content, 'html.parser')
            links = get_internal_links(main_soup, base_url)
            content_by_link = {}

            for link in links:
                content = scrape_content(link)
                if content:
                    content_by_link[link] = content
                time.sleep(1)  # Delay between requests to avoid hitting the server too hard

            # Generate PDFs for each category/link
            for idx, (link, content) in enumerate(content_by_link.items(), 1):
                filename = f"scraped_data_{idx}.pdf"
                generate_pdf(content, filename)

            print("All PDFs generated successfully.")
        else:
            print(f"Failed to retrieve main page content, status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
 