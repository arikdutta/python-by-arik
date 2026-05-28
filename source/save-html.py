import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
 
 
url = "https://www.iconicsmart.in/product-page/cl-32l50n-led-tv"
 
response = requests.get(url)
 
soup = BeautifulSoup(response.text, "html.parser")
 
 
img = soup.find("picture")
 
img_url = img.get("src")
 
 
full_img_url = urljoin(url, img_url)
 
print(full_img_url)
 
 
image = requests.get(full_img_url)
 
 
file = open("downloaded.jpg", "wb")
 
file.write(image.content)
 
file.close()
 
print("Image Downloaded Successfully")