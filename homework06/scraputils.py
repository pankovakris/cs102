import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    posts = parser.findAll("tr")[3]
    news = posts.td.find_all("tr", attrs={"class": "athing"})
    content = posts.td.find_all("td", attrs={"class": "subtext"})
    for i in range(len(news)):
        if content[i].find("a", attrs={"class": "hnuser"}):
            author = content[i].find("a", attrs={"class": "hnuser"}).text.split()[0]
        else:
            author = None

        if content[i].find("span", attrs={"class": "score"}):
            points = int(
                content[i].find("span", attrs={"class": "score"}).text.split()[0]
            )
        else:
            points = 0

        comms = content[i].find_all("a")[-1].text
        if comms == "discuss":
            comms = 0
        else:
            comms = comms.split()[0]

        news_list.append(
            {
                "author": author,
                "comments": comms,
                "points": points,
                "title": news[i].find("a", attrs={"class": "titlelink"}).text,
                "url": news[i].find("a", attrs={"class": "titlelink"})["href"],
            }
        )

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    body = parser.findAll("tr")[3]
    return body.td.find_all("td", attrs={"class": "title"})[-1].a["href"]


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


# print(get_news("https://news.ycombinator.com/", 3))
