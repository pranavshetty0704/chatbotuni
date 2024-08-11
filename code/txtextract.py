import os
from PyPDF2 import PdfReader

# Function to extract text from a single PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Directory (folder) containing the PDFs
pdf_directory = r"C:\Users\Shagun\Downloads\chatbotuni-main\chatbotuni-main\scrapped data"

# Directory where the extracted text files will be saved
output_directory = r"C:\Users\Shagun\Downloads\chatbotuni-main\chatbotuni-main\extracted_text"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Extract text from all PDFs in the directory (folder)
for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, filename)
        text = extract_text_from_pdf(pdf_path)
        
        # Save the extracted text to a .txt file in the output directory
        output_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(output_directory, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as text_file:
            text_file.write(text)

print("Text extraction complete! The extracted texts are saved in:", output_directory)
