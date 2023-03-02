import requests
import random
import os
from datetime import datetime


def read_links_from_file(file):
    with open(file, 'r') as f:
        links = [s[:-1] for s in f.readlines()]
    return links


def select_valid_link(links):

    def select_random(links):
        link = links[random.randint(0, len(links)-1)]
        return link
    
    def is_valid(link):
        with requests.get(link, stream=True) as r:
            return True if r.status_code == 200 else False
    
    count = 0
    while True:
        link = select_random(links)
        if is_valid(link):
            break
        count += 1
        if count > len(links):
            raise Exception('No valid link')
    return link


def download(url):
    local_filename = url.split('/')[-1]
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
    
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    
                return local_filename


def delete(file):
    os.remove(file)

def main():
    try:
        links_file = 'links.txt'
        links = read_links_from_file(links_file)
        url = select_valid_link(links)
        file_name = download(url)
        delete(file_name)
    except Exception as e:
        with open('logs.txt', 'w+') as f:
            f.write(f'{str(e)} {datetime.now()}\n')

if __name__ == "__main__":
    main()
