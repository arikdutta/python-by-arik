import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

NEWS_URL = "https://www.bbc.com/news"
REFRESH_INTERVAL = 60  # 1 hour in seconds
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif")


def make_run_folders():
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    img_dir = os.path.join("bbc_downloads", timestamp, "images")
    pdf_dir = os.path.join("bbc_downloads", timestamp, "pdfs")
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)
    return img_dir, pdf_dir


def download_file(url, dest_path):
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    with open(dest_path, "wb") as f:
        f.write(response.content)


def scrape_bbc(url):
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Scraping: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    img_dir, pdf_dir = make_run_folders()

    # ======================
    # DOWNLOAD IMAGES
    # ======================
    image_count = 0
    print("\n--- Images ---")
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or ""
        if not src:
            continue
        if not any(ext in src.lower() for ext in IMAGE_EXTENSIONS):
            continue
        img_url = urljoin(url, src)
        ext = next((e for e in IMAGE_EXTENSIONS if e in src.lower()), ".jpg")
        filename = os.path.join(img_dir, f"image_{image_count + 1}{ext}")
        try:
            download_file(img_url, filename)
            print(f"  Downloaded: {filename}")
            image_count += 1
        except Exception as e:
            print(f"  Image error ({img_url}): {e}")

    # ======================
    # DOWNLOAD PDFs
    # ======================
    pdf_count = 0
    print("\n--- PDFs ---")
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if ".pdf" not in href.lower():
            continue
        pdf_url = urljoin(url, href)
        filename = os.path.join(pdf_dir, f"pdf_{pdf_count + 1}.pdf")
        try:
            download_file(pdf_url, filename)
            print(f"  Downloaded: {filename}")
            pdf_count += 1
        except Exception as e:
            print(f"  PDF error ({pdf_url}): {e}")

    # ======================
    # SAVE ALL LINKS
    # ======================
    links_file = os.path.join("bbc_downloads", time.strftime("%Y-%m-%d_%H-%M-%S") + "_links.txt")
    all_links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
    with open(links_file, "w", encoding="utf-8") as f:
        f.write("\n".join(all_links))
    print(f"\nLinks saved: {links_file}")

    print(f"Summary: {image_count} image(s) downloaded, {pdf_count} PDF(s) downloaded.")


while True:
    scrape_bbc(NEWS_URL)
    next_run = time.strftime("%H:%M:%S", time.localtime(time.time() + REFRESH_INTERVAL))
    print(f"\nNext refresh at {next_run} (in 1 hour). Press Ctrl+C to stop.")
    time.sleep(REFRESH_INTERVAL)
