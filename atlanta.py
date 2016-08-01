from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle

#bad_links = ("https://www.frbatlanta.org//news/speeches/2007/071107-lockhart.aspx", "https://www.frbatlanta.org//news/speeches/2007/070928-lockhart.aspx", "https://www.frbatlanta.org//news/speeches/2007/070906-lockhart.aspx", "https://www.frbatlanta.org//news/speeches/2008/081215-frame.aspx", "https://www.frbatlanta.org//news/speeches/2008/081107-lockhart.aspx", "https://www.frbatlanta.org//news/speeches/2008/081020-lockhart.aspx")
bad_links = []
speeches = []
for year in range(2006, 2017):
    html = urlopen("https://www.frbatlanta.org/news/speeches/?pub_year=" + str(year))
    soup = BeautifulSoup(html, 'html.parser')

    base_links = soup.findAll("div", {"class", "cols6of12"})[0]
    base_links = base_links.find_all("a")
    base_links = list(filter(lambda x: ".pdf" not in x, map(lambda y: y.attrs["href"], base_links)))


    base_url = "https://www.frbatlanta.org/"

    for link in base_links:
        url = base_url + link
        print(url)
        if url in bad_links:
            continue
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')

        try:
            title_div = soup.findAll("h2", {"class": "typeHighlight1"})[0]
            print(title_div)
        
        except IndexError:
            bad_links.append(url)
            continue

        title = list(title_div.children)[0].get_text()

        divs = soup.findAll("div", {"class": "col cols6of12"})
        
        content = divs[0]
        count = 0
        speech_text = ""
        for child in content.children:
            # we only want child tags that are <p> or <h3>, the divs are the notes
            # which we don't want
            if (child.name == "p"):
                count = count + 1
                if count > 1:
                    speech_text += child.get_text() + " "

        if link[24] == int:                
            print("hi")
            date = link[19:25] # TODO: make this general and assert it's date
            date = date[:2] + "-" + date[2:4] + "-" + date[4:]
            print(date, title)
        else:
            date = link[17:24]
            date = date[:2] + "-" + date[3:5] + "-" + date[5:]
            print(date, title)

        speech = {"title": title,
                  "date": date,
                  "url": link,
                  "text": speech_text}

        speeches.append(speech)

pickle.dump(speeches, open("./data/atlantafed_dump.pkl", "wb"))
