from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle

speeches = []
html = urlopen("https://www.bostonfed.org/news-and-events/speeches.aspx")
soup = BeautifulSoup(html, 'html.parser')
link_container = soup.find("div", "panel-group frb")
#year_containers = soup.find_all("div", "article-list-container")
speech_rows = link_container.find_all("div", "row")
base_url = "https://www.bostonfed.org"
for row in speech_rows:
    title = row.find("h1", "card-title")
    if title is None:
        # empty row, on to the next
        continue

    link = title.find("a").attrs["href"]
    title_text = title.get_text()[1:]
    date = row.find("small", "action").get_text()

    speech_html = urlopen(base_url + link)
    speech_soup = BeautifulSoup(speech_html, 'html.parser')

    author = speech_soup.find("a", "byline-link").get_text()

    speech_para = speech_soup.find("div", "bodytextlist").find_all("p")
    speech_text = ""
    for para in speech_para:
        if len(para.find_all("em")) > 0:
            # getting rid of the blurb at the end saying who made the speech and where
            continue

        speech_text += para.get_text() + " "

    speeches.append({"title": title_text,
                     "date": date,
                     "author": author,
                     "text": speech_text})
    print(title_text, date, author)

with open("./data/boston.pkl", "wb") as f:
    pickle.dump(speeches, f)

