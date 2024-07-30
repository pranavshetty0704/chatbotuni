from fpdf import FPDF
import requests
from bs4 import BeautifulSoup

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Scraped Data', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_chapter(self, title, body):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(body)

def fetch_and_generate_pdf(url, pdf_filename):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Send the request with headers
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # Set the encoding to UTF-8
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Customize your scraping logic based on the structure of the page
    title = soup.find('title').get_text(strip=True)
    content = soup.get_text(separator='\n', strip=True)

    # Create PDF
    pdf = PDF()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    pdf.add_chapter(title, content)

    # Save the PDF
    pdf.output(pdf_filename)

# Example usage
urls = [
    "https://vcet.edu.in/",
    "https://vcet.edu.in/32-2/",
    "https://vcet.edu.in/about-alumni-2/",
    "https://vcet.edu.in/academics/",
    "https://vcet.edu.in/about-us/",
    # Add more URLs as needed
]

for index, url in enumerate(urls, start=1):
    try:
        pdf_filename = f"scraped_data_{index}.pdf"
        fetch_and_generate_pdf(url, pdf_filename)
        print(f"PDF generated: {pdf_filename}")
    except Exception as e:
        print(f"Error generating PDF for {url}: {e}")
