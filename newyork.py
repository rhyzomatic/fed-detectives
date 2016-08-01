from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle

speeches = []
with open("./html_data/newyork.html", "r") as f:
    html = f.read()
soup = BeautifulSoup(html, 'html.parser')
link_table = soup.find("table", "newsTable")
years_rows = link_table.find_all("tbody")
base_url = "https://www.newyorkfed.org"
for row in (r for year in years_rows for r in year.find_all("tr")):
    if "yrHead" in row.attrs["class"]:
        # this is header row
        continue

    date = row.find("td", "dirColL").get_text().replace("\n", "")

    link = row.find("a", "paraHeader").attrs["href"]
    title_text = row.find("div", "tablTitle").get_text().replace("\n", "")

    speech_html = urlopen(base_url + link)
    speech_soup = BeautifulSoup(speech_html, 'html.parser')

    speech_para = speech_soup.find("div", "ts-article-text").find_all("p")
    speech_text = ""
    for para in speech_para[:-1]:
        speech_text += para.get_text() + " "

    speeches.append({"title": title_text,
                     "date": date,
                     "text": speech_text})
    print(title_text, date)

with open("./data/newyork.pkl", "wb") as f:
    pickle.dump(speeches, f)

