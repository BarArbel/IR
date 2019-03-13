import requests
from bs4 import BeautifulSoup


def lyrics_crawler(max_pages):
    page = 0
    while page < max_pages:
        url = "https://www.lyrics.com/random.php"
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "lxml")
        s_find = soup.find("h1", {"id": "lyric-title-text"})
        song_title = s_find.string
        print(song_title)
        s_find = soup.find("div", {"class": "artist-meta"})
        artist = s_find.get("h4").string
        print(artist)
        page += 1


lyrics_crawler(1)
