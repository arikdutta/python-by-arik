import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
 
 
url = {"https://static.wixstatic.com/media/fbffc6_dcc1026e…o/fbffc6_dcc1026e2a674acea9d32a2d6d5ffb41~mv2.jpg","https://static.wixstatic.com/media/fbffc6_830d8d1d…o/fbffc6_830d8d1de3924d3c8c0c4074f6c480b1~mv2.jpg"}
 
response = requests.get(url)
 
soup = BeautifulSoup(response.text, "html.parser")
 
 
img = soup.find("img")
 
img_url = img.get("src")
 
 
full_img_url = urljoin(url, img_url)
 
print(full_img_url)
 
 
image = requests.get(full_img_url)
 
 
file = open("downloaded-image-all.jpg", "wb")
 
file.write(image.content)
 
file.close()
 
print("Image Downloaded Successfully")