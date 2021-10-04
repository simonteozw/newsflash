import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline

requests.packages.urllib3.disable_warnings()
# Create your views here.
def scrape(request):
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = "https://www.theonion.com/"

    content = session.get(url, verify=False).content
    soup = BSoup(content, "html.parser")
    News = soup.find_all('div', {"class":"js_curation-block-list"})
    # web scraping part is not well done. the onion website is complicated
    for story in News:
        for article in story:
            if len(article.find_all('a')) == 0:
                continue
            main = article.find_all('a')[0]
            if main.find('img') is None or main.find('title') is None:
                continue
            link = main['href']
            image_src = str(main.find('img')['srcset']).split(" ")[0]
            title = main['title']
            new_headline = Headline()
            new_headline.title = title
            new_headline.url = link
            new_headline.image = image_src
            new_headline.save()
    return redirect("../")

def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        'object_list': headlines,
    }
    return render(request, "news/home.html", context)