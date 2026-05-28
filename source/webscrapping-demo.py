import requests
from bs4 import BeautifulSoup
 
url = "https://www.iana.org/help/example-domains"
 
response = requests.get(url)
 
soup = BeautifulSoup(response.text, "html.parser")
 
headings = soup.find_all("img")
 
for h in headings:
 
    print(h.text)
    
    
    