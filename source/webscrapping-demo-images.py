import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

output_dir = "downloaded-images"
url = "https://en.wikipedia.org/wiki/Cat"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

os.makedirs(output_dir, exist_ok=True)

images = soup.find_all("img")

count = 1

for img in images:

    src = img.get("src")

    if not src or "upload.wikimedia.org" not in src:
        continue

    full_url = urljoin(url, src)

    image = requests.get(full_url)

    file = open(f"downloaded-images/cat_{count}.jpg", "wb")

    file.write(image.content)

    file.close()

    print(f"Image {count} Downloaded")

    count += 1

print(f"\nDone. Images saved to '{output_dir}/'")