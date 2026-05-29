import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

output_dir = "downloaded-new-images"
url = "https://www.iconicsmart.in/category/washing-machine"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
os.makedirs(output_dir, exist_ok=True)
images = soup.find_all("img")

count = 1

for img in images:
   img_url = img.get("src")
   full_url = urljoin(url, img_url)
   print(full_url)
   image = requests.get(full_url)
   file = open(f"{output_dir}/washing_machine_{count}.jpg", "wb")
   file.write(image.content)
   file.close()
   print(f"Image {count} Downloaded")
   count += 1
   
   print(f"\nDone. Images saved to '{output_dir}/'")