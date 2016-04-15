from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle

html = urlopen("https://www.chicagofed.org/publications/speeches/index")
soup = BeautifulSoup(html, 'html.parser')

base_links = soup.findAll("div", {"class", "links"})[0]
base_links = base_links.find_all("a")
base_links = list(filter(lambda x: ".pdf" not in x, map(lambda y: y.attrs["href"], base_links)))
print(base_links)

base_url = "https://www.chicagofed.org"
speeches = []

for l in base_links:
    url = base_url + l
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    mydivs = soup.findAll("div", { "class" : "content-text"})
    links = mydivs[0].find_all("a")

    hrefs = []
    for link in links:
        hrefs.append(link.attrs["href"])

    links = list(filter(lambda x: (".pdf" not in x) and (".cfm" not in x), hrefs))

    print("Links have been gotten")
    print(links)

    for link in links:
        html = urlopen(base_url + link)
        soup = BeautifulSoup(html, 'html.parser')

        title_div = soup.findAll("div", {"class": "detail-title"})[0]
        title = list(title_div.children)[0].get_text()

        divs = soup.findAll("div", {"class": "content-text"})
        if (len(divs) < 1):
            divs = soup.findAll("div", {"class": "detail-introduction"})

        content = divs[0]

        speech_text = ""
        for child in content.children:
            # we only want child tags that are <p> or <h3>, the divs are the notes
            # which we don't want
            if (child.name in ("p", "h3")):
                speech_text += child.get_text() + " "

        date = link[28:36] # TODO: make this general and assert it's date

        print(date, title)

        speech = {"title": title,
                  "date": date,
                  "url": link,
                  "text": speech_text}

        speeches.append(speech)


pickle.dump(speeches, open("chicagofed_dump.pkl", "wb"))


