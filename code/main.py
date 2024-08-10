import requests
from bs4 import BeautifulSoup

# URL of the website you want to scrape
url = 'https://vcet.edu.in/'

# Custom headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Send the request with headers
response = requests.get(url, headers=headers)


soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify)

title = soup.title

paras = soup.find_all('p')
   
print(soup.find('a')) 
  

print(soup.find('p').get_text()) 

print(soup.get_text())

anchors = soup.find_all('a')
all_links = set()

for link in anchors:
    if(link.get('href') != '#'):
       linkText = "https://vcet.edu.in/" +link.get('href')
       all_links.add(link)
       print(linkText)   
