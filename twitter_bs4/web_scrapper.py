import json
import os
import re
import sys

from datetime import datetime

import requests

from bs4 import BeautifulSoup


get_num = lambda s: re.search(r'(?<=\s)\d+', s).group()

def get_html(url):
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, 'html.parser')

    for tweet in content.find_all('div', attrs={'class': 'tweetcontainer'}):
        tweet_data = {
            'author': tweet.find('h2', attrs={'class': 'author'}).text,
            'date': tweet.find('h5', attrs={'class': 'dateTime'}).text,
            'tweet': tweet.find('p', attrs={'class': 'content'}).text,
            'likes': get_num(tweet.find('p', attrs={'class': 'likes'}).text),
            'shares': get_num(tweet.find('p', attrs={'class': 'shares'}).text)
        }

        yield tweet_data

def scrape_to_json(url):
    now = datetime.now()

    current_time = now.strftime('%Y-%m-%d_%H:%M')
    file_path = f'data/twitter_data{current_time}.json'

    with open(file_path, 'a') as f:
        for data in get_html(url):
            json.dump(data, f)
            f.write('\n')



if __name__ == '__main__':
    url = sys.argv[1]
    scrape_to_json(url)
