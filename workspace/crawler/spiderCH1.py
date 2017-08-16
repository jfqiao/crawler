from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup


def get_title(url):
    try:
        html = urlopen(url)
    except HTTPError:
        return None
    try:
        bs_obj = BeautifulSoup(html.read(), 'lxml')
        title = bs_obj.body.h1
    except AttributeError:
        return None
    return title


def test_ch1():
    title = get_title("http://www.pythonscraping.com/pages/page1.html")
    if title is None:
        print("Page not found")
    else:
        print(title)

