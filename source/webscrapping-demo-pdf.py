import requests
from bs4 import BeautifulSoup

url = "https://www.coroners.nsw.gov.au/coronial-findings-search.html"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

pdf_links = []

for a in soup.find_all("a", href=True):
    if a["href"].lower().endswith(".pdf"):
        pdf_links.append(a["href"])

print(pdf_links[:5])  # show first few
