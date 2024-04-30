import re
import requests
import os

# 放你网易云的复制链接到这里， 形式 链接：歌的名字
songs = {
    "https://music.163.com/song?id=1907868691&userid=514157754": "地基街头",
    "https://music.163.com/dj?id=2535580578&userid=514157754": "upNeverdown",
    "https://music.163.com/song?id=2148786274&userid=514157754": "KASABLANCA",
    "https://music.163.com/song?id=2146490314&userid=514157754" : "BRAZIL",
    "https://music.163.com/song?id=2009226782&userid=514157754" : "BAD BAD",
    # Add more entries as needed
}

def process_links(songs):
    new_urls = []
    for link in songs.keys():
        match = re.search(r"id=(\d+)", link)
        if match:
            song_id = match.group(1)
            new_url = f"http://music.163.com/song/media/outer/url?id={song_id}.mp3"
            new_urls.append((new_url, songs[link]))
    return new_urls

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
            print(f'Downloaded and renamed to: {final_name}, 文件在你这个文件一样的目录里')
        else:
            print(f'Failed to download from {url}')

songs_info = process_links(songs)

download_and_rename_mp3(songs_info)
