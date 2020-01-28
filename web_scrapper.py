import sys

import requests

from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, 'html.parser')

    for tweet in content.find_all('div', attrs={'class': 'tweetcontainer'}):
        tweet_data = {
            'author': tweet.find('h2', attrs={'class': 'author'}).text,
            'date': tweet.find('h5', attrs={'class': 'dateTime'}).text,
            'tweet': tweet.find('p', attrs={'class': 'content'}).text,
            'likes': tweet.find('p', attrs={'class': 'likes'}).text,
            'shares': tweet.find('p', attrs={'class': 'shares'}).text
        }

        yield tweet_data


if __name__ == '__main__':
    url = sys.argv[1]
    content = get_html(url)
    print(next(content))
