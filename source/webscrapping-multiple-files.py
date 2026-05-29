import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
# Websites to scrape
websites = [
   "https://www.iconicsmart.in/category/washing-machine",
   "https://www.coroners.nsw.gov.au/coronial-findings-search.html"
]
# Create folders
os.makedirs("images", exist_ok=True)
os.makedirs("pdfs", exist_ok=True)
# Store all links
all_links = []
image_count = 1
pdf_count = 1
for website in websites:
   print(f"\nScraping: {website}")
   try:
       response = requests.get(website, timeout=10)
       soup = BeautifulSoup(response.text, "html.parser")
       # ======================
       # SCRAPE ALL LINKS
       # ======================
       links = soup.find_all("a")
       for link in links:
           href = link.get("href")
           if href:
               full_link = urljoin(website, href)
               all_links.append(full_link)
       # ======================
       # DOWNLOAD IMAGES
       # ======================
       images = soup.find_all("img")
       for img in images:
           src = img.get("src")
           if src:
               img_url = urljoin(website, src)
               try:
                   img_response = requests.get(img_url, timeout=10)
                   content_type = img_response.headers.get(
                       "Content-Type", ""
                   )
                   if "image" in content_type:
                       extension = content_type.split("/")[-1]
                       filename = f"images/image_{image_count}.{extension}"
                       with open(filename, "wb") as file:
                           file.write(img_response.content)
                       print(f"Downloaded: {filename}")
                       image_count += 1
               except Exception as e:
                   print("Image Error:", e)
       # ======================
       # DOWNLOAD PDFS
       # ======================
       for link in links:
           href = link.get("href")
           if href and ".pdf" in href.lower():
               pdf_url = urljoin(website, href)
               try:
                   pdf_response = requests.get(pdf_url)
                   filename = f"pdfs/pdf_{pdf_count}.pdf"
                   with open(filename, "wb") as file:
                       file.write(pdf_response.content)
                   print(f"Downloaded: {filename}")
                   pdf_count += 1
               except Exception as e:
                   print("PDF Error:", e)
   except Exception as e:
       print("Website Error:", e)
# ======================
# SAVE ALL LINKS
# ======================
with open("all_links.txt", "w", encoding="utf-8") as file:
   for link in all_links:
       file.write(link + "\n")
print("\nScraping Completed Successfully")