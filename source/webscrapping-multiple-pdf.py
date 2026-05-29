import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

output_dir = "downloaded-new-pdfs"
url = "https://www.coroners.nsw.gov.au/coronial-findings-search.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
os.makedirs(output_dir, exist_ok=True)
pdfs = soup.find_all("a")

count = 1

for pdf in pdfs:
   pdf_url = pdf.get("href")
   if pdf_url and ".pdf" in pdf_url:
       pdf_url1 = urljoin(url, pdf_url)
       print(pdf_url1)
       pdf = requests.get(pdf_url1)
       file = open(f"{output_dir}/pdf_{count}.pdf", "wb")
       file.write(pdf.content)
       file.close()
       print(f"PDF {count} Downloaded")
       count += 1
   

print(f"\nDone. PDFs saved to '{output_dir}/'")