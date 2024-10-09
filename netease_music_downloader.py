import re
import requests
from bs4 import BeautifulSoup
import os

# 网易云音乐链接列表
songs = [
    "https://music.163.com/song?id=2042350565&userid=9834375319",
    "https://music.163.com/song?id=1832633339&userid=9834375319",
    "https://music.163.com/song?id=2139033163&userid=9834375319",
    # Add more URLs as needed
]

def process_links(songs):
    new_urls = []
    for link in songs:
        match = re.search(r"id=(\d+)", link)
        if match:
            song_id = match.group(1)
            new_url = f"http://music.163.com/song/media/outer/url?id={song_id}.mp3"
            song_name = fetch_song_title(link)
            new_urls.append((new_url, song_name))
    return new_urls

def fetch_song_title(song_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(song_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        # Look for the title tag or any meta tag containing the song name
        title_tag = soup.find('title')
        if title_tag:
            # Clean up the title by removing any extra text (like "网易云音乐" or "- 网易云音乐")
            title = title_tag.text.strip().split('-')[0].strip()
            print(f"Found song title: {title}")
            return title
    return "Unknown Title"

def download_and_rename_mp3(songs_info):
    for url, name in songs_info:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            temp_file_name = url.split('id=')[-1]
            with open(temp_file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            final_name = f"{name}.mp3"
            os.rename(temp_file_name, final_name)

            # Get absolute path of the saved file
            final_path = os.path.abspath(final_name)
            print(f'Downloaded and renamed to: {final_name}')
            print(f'File stored at: （文件放在了:） {final_path}')
        else:
            print(f'Failed to download from {url}')

songs_info = process_links(songs)

download_and_rename_mp3(songs_info)
