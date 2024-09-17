import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from datetime import datetime

def enforce_search_page(url, page_number):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params['search_page'] = [str(page_number)]
    
    new_query_string = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query_string))
    return new_url

def create_download_folder():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    folder_name = f"stolen-{datetime.now().strftime('%Y-%m-%d')}"
    folder_path = os.path.join(desktop, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    return folder_path

def download_images(url, save_folder):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Collect all <meta itemprop="thumbnailUrl"> tags
    meta_tags = soup.find_all('meta', itemprop='thumbnailUrl')
    img_urls = [(meta_tag['content'], meta_tag.find_previous_sibling('meta', itemprop='name')['content'])
                for meta_tag in meta_tags]

    for idx, (img_url, alt_text) in enumerate(img_urls):
        try:
            img_data = requests.get(img_url).content
            # Remove illegal characters from alt text for file naming
            clean_alt_text = ''.join(e for e in alt_text if e.isalnum() or e in (' ', '-', '_')).strip()
            img_name = f"{clean_alt_text}.jpg" if clean_alt_text else f"image_{idx+1}.jpg"
            
            with open(os.path.join(save_folder, img_name), 'wb') as handler:
                handler.write(img_data)
            print(f"Downloaded {img_name} from {url}")
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python longFingers.py <initial_url> <number_of_pages>")
        sys.exit(1)

    initial_url = sys.argv[1]
    num_pages = int(sys.argv[2])
    save_folder = create_download_folder()

    for page_num in range(1, num_pages + 1):
        modified_url = enforce_search_page(initial_url, page_num)
        print(f"Fetching images from: {modified_url}")
        download_images(modified_url, save_folder)
