import requests
from bs4 import BeautifulSoup
import re


def english_chars_check(s):
    try:
        s.encode(encoding="utf-8").decode("ascii")
    except UnicodeDecodeError:
        return False
    return True


def lyrics_crawler(max_pages):
    page = 0
    while page < max_pages:
        url = "https://www.lyrics.com/random.php"
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "lxml")
        try:
            s_find = soup.find("h1", {"id": "lyric-title-text"})
            song_title = s_find.string
            if english_chars_check(song_title) is False:
                continue
            print(song_title)
            s_find = soup.find("div", {"class": "artist-meta"})
            artist = s_find.find("h4").string
            artist = artist.split(",")[0]
            if english_chars_check(artist) is False:
                continue
            print(artist)
            s_find = soup.find("pre", {"id": "lyric-body-text"})
            lyrics = re.sub("<[^>]+>", "", str(s_find))
            if english_chars_check(lyrics) is False:
                continue
            print()
            print(lyrics)
        except:
            continue

        filePtr = open("files/files_to_add/"+song_title+".txt", "w")
        filePtr.write(artist+",Song\n\n")
        filePtr.write(lyrics)

        page += 1


lyrics_crawler(1)
