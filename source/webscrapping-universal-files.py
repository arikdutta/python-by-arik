import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

image_url = "https://www.iconicsmart.in/category/washing-machine"
response = requests.get(image_url)
soup = BeautifulSoup(response.text, "html.parser")
pdfs = soup.find_all("a")
images = soup.find_all("img")
count_img = 1

pdfs_url = "https://www.coroners.nsw.gov.au/coronial-findings-search.html"
response_pdfs = requests.get(pdfs_url)
soup = BeautifulSoup(response_pdfs.text, "html.parser")
pdfs = soup.find_all("a")
count_pdfs = 1

for pdf in pdfs:
   pdf_url = pdf.get("href")
   if pdf_url and ".pdf" in pdf_url:
       pdf_url1 = urljoin(pdfs_url, pdf_url)
       print("PDF URLs:", pdf_url1)
       count_pdfs += 1


for img in images:
   img_url = img.get("src")
   if img_url and ".jpg" in img_url:
       img_url1 = urljoin(image_url, img_url)
       print("Image URLs:", img_url1)
       print(f"Image {count_img} Downloaded")
       count_img += 1

print(f"\nDone. Images and Pdfs saved")