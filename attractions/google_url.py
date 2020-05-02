import urllib.parse
from googlesearch import search


def get_url():
    query = "Достопримечательности спб"

    urls = []
    url_for_me = ['https://www.tripzaza.com/ru/destinations/luchshie-dostoprimechatelnosti-sankt-peterburga/',
                  'https://top10.travel/dostoprimechatelnosti-sankt-peterburga/',
                  'https://spb.sutochno.ru/info/gorod']
    for j in search(query, lang="ru", tld="ru", num=15, stop=15, pause=3):
        if urllib.parse.unquote(j) in url_for_me:
            urls.append(j)
    return urls
