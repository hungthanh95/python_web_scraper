import requests
from bs4 import BeautifulSoup
import string
import os


def check_url(url):
    if "nature.com/nature/articles" in url:
        return True
    else:
        return False


# get input: 1 -> number of page, 2 -> type of article
num_pages = int(input())
type_of_article = str(input())

# loop all pages
for page in range(1, num_pages + 1):
    url_req = "https://www.nature.com/nature/articles"
    url_req = url_req + '?page=' + str(page)
    page_dir = 'Page_' + str(page)

    # r = requests.get(url_req, headers={'Accept-Language': 'en-US,en;q=0.5'})
    r = requests.get(url_req)

    # check if dir exist or not
    if not os.path.isdir(page_dir):
        os.mkdir(page_dir)

    if r.ok and check_url(url_req):
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.select('li.app-article-list-row__item')
        for article in articles:
            article_type = article.select('span[data-test="article.type"]')[0].text.strip()
            if article_type == type_of_article:
                news = article.select('a[data-track-action="view article"]')
                link = "https://www.nature.com" + news[0]['href']
                title = news[0].text.strip()
                # remove punctuation
                title = title.translate(str.maketrans('', '', string.punctuation))
                # remove whitespace
                title = title.replace(' ', '_')

                article_request = requests.get(link)
                article_soup = BeautifulSoup(article_request.content, 'html.parser')
                article_body = article_soup.select('div .article-item__body p')
                if not article_body:
                    article_body = article_soup.select('div .article__body p')
                print(article_body)
                with open(os.path.join(page_dir, title + '.txt'), 'w', encoding="utf-8") as file:
                    for body in article_body:
                        file.write(body.text)

                print("Save done article: " + title)
    else:
        print('Invalid article page!')
