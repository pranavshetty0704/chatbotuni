import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from urllib.parse import urljoin, urlparse
import os

# Base URL of the website
base_url = "https://vcet.edu.in/"

# Function to get all links from a page
def get_links(soup, base_url):
    links = set()
    for anchor in soup.find_all('a', href=True):
        link = urljoin(base_url, anchor['href'])
        if base_url in link and urlparse(link).netloc == urlparse(base_url).netloc:
            links.add(link)
    return links

# Function to scrape content from a URL
def scrape_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            page_soup = BeautifulSoup(response.content, 'html.parser')
            content = []
            for heading in page_soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                content.append(heading.get_text(strip=True))
            for paragraph in page_soup.find_all('p'):
                content.append(paragraph.get_text(strip=True))
            return content
        else:
            print(f"Failed to retrieve content from {url}")
            return []
    except Exception as e:
        print(f"Error while scraping {url}: {e}")
        return []

# Function to generate PDF from scraped data
def generate_pdf(data, filename):
    try:
        if not data:
            print(f"No content to write for {filename}")
            return

        pdf = PDF()
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)
        pdf.add_page()
        for content in data:
            if content:
                if isinstance(content, str):
                    content = content.encode('latin-1', 'replace').decode('latin-1')
                pdf.chapter_body(content)
        pdf.output(filename)
        print(f"PDF generated: {filename}")
    except Exception as e:
        print(f"Error generating PDF {filename}: {e}")


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Scraped Data', 0, 1, 'C')
        self.ln(10)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

# Main scraping process
try:
    response = requests.get(base_url)
    main_soup = BeautifulSoup(response.content, 'html.parser')

    # Get all links from the main page
    links = get_links(main_soup, base_url)

    # Dictionary to hold content categorized by link
    content_by_link = {}

    for link in links:
        content = scrape_content(link)
        content_by_link[link] = content

    # Generate PDFs for each category/link
    for idx, (link, content) in enumerate(content_by_link.items(), 1):
      filename = f"scraped_data_{idx}.pdf"
      print(f"Generating PDF for {link} with {len(content)} items.")
      generate_pdf(content, filename)

    print("All PDFs generated successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

import os

print("Current working directory:", os.getcwd())
