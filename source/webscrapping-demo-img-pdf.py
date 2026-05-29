import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.ncei.noaa.gov/access/paleo-search/"

# Create folders
os.makedirs("pdfs", exist_ok=True)
os.makedirs("images", exist_ok=True)

# Fetch page
html = requests.get(BASE_URL).text
soup = BeautifulSoup(html, "html.parser")

# Lists to store links
pdf_links = []
image_links = []

# Extract PDF links
for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.lower().endswith(".pdf"):
        pdf_links.append(urljoin(BASE_URL, href))

# Extract image links
for img in soup.find_all("img"):
    src = img.get("src")
    if src:
        image_links.append(urljoin(BASE_URL, src))

# Download PDFs
for link in pdf_links:
    filename = os.path.join("pdfs", link.split("/")[-1])
    print("Downloading PDF:", filename)
    with open(filename, "wb") as f:
        f.write(requests.get(link).content)

# Download Images
for link in image_links:
    filename = os.path.join("images", link.split("/")[-1])
    print("Downloading Image:", filename)
    with open(filename, "wb") as f:
        f.write(requests.get(link).content)

print("Done! PDFs saved in /pdfs and images saved in /images")
