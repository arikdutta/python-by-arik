import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
 
 
url = "https://unsplash.com/blog/introducing-unsplash-photos-for-google-slides/"
 
response = requests.get(url)
 
soup = BeautifulSoup(response.text, "html.parser")
 
images = soup.find_all("img")
 
 
count = 1
 
 
for img in images:
 
    img_url = img.get("src")
 
    full_url = urljoin(url, img_url)
 
    print(full_url)
 
    image = requests.get(full_url)
 
    file = open(f"image_{count}.jpg", "wb")
 
    file.write(image.content)
 
    file.close()
 
    print(f"Image {count} Downloaded")
 
    count += 1