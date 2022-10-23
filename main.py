import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def get_first_news():
    # создаем  словарь заголовков
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.3.886 Yowser/2.5 Safari/537.36"
    }

    url = "https://www.rbc.ru/short_news"

    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")

    articles_cards = soup.find_all("div", class_="js-news-feed-item js-yandex-counter")

    today = str(datetime.now().date())

    news_dict = {}
    for article in articles_cards:
        article_title = article.find("span", class_="item__title rm-cm-item-text").text.strip()
        article_url = article.find('a', class_='item__link').get("href")
        article_date_time = article.find("span", class_="item__category").text.strip()

        article_id = article_url
        # print(f"{article_title} | {article_url} | {article_date_time}")

        news_dict[article_id] = {
            "article_date_time": article_date_time + ' ' + today,
            "article_title": article_title,
            "article_url": article_url
        }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open("news_dict.json") as file:
        news_dict = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.3.886 Yowser/2.5 Safari/537.36"
    }

    url = "https://www.rbc.ru/short_news"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="js-news-feed-item js-yandex-counter")

    fresh_news = {}
    for article in articles_cards:
        article_url = article.find('a', class_='item__link').get("href")
        article_id = article_url

        if article_id in news_dict:
            continue
        else:
            article_title = article.find("span", class_="item__title rm-cm-item-text").text.strip()
            article_date_time = article.find("span", class_="item__category").text.strip()

            news_dict[article_id] = {
                "article_date_time": article_date_time,
                "article_title": article_title,
                "article_url": article_url
            }

            fresh_news[article_id] = {
                "article_date_time": article_date_time,
                "article_title": article_title,
                "article_url": article_url
            }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    print(check_news_update())
    get_first_news()


if __name__ == '__main__':
    main()