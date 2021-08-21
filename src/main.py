from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import configparser
import requests
import re


def test_keywords(url_list, keywords):

    c_keys = []
    for url in url_list:
        print(f"Checking keywords in url {url}")
        r = requests.get(url)
        s = BeautifulSoup(r.content, "html.parser")
        txt_body = r_tags(s.find("div", {"itemprop": "articleBody"})).lower()

        keys = ''
        for key in keywords:
            if key in txt_body:
                keys= keys + key + ' '
        c_keys.append(keys)
        print(keys)
    return c_keys

def load_configs(path):

    config = configparser.ConfigParser()
    config.read(path)
    return config

def r_tags(element):

    remove_tags = re.compile(r'<[^>]+>')
    out = remove_tags.sub('', str(element))
    out = out.replace('\n', '')
    return out

def try_date(date_str):

    format_str = '%d/%m/%Y'
    try:
        out = datetime.strptime(date_str, format_str)
    except:
        out = datetime.fromtimestamp(0).strftime(format_str)
    return out

def create_df(soup, keywords):

    # select contests
    contests = soup.find_all("div", attrs={"class": "ca"})
    c_role, c_state, c_until, c_title, c_url = [], [], [], [], []
    for cnt in contests:
        c_role.append(r_tags(str(cnt.select_one('span')).rsplit('br')[0][:-1]))
        c_state.append(r_tags(cnt.select('div')[1]))
        date_str = try_date(r_tags(cnt.select('div')[3])[-10:])
        c_until.append(date_str)
        c_title.append(cnt.select('a')[0].get('title'))
        c_url.append(cnt.select('a')[0].get('href'))
    c_keys = test_keywords(c_url, keywords)

    df = pd.DataFrame(list(zip(c_role, c_state, c_until, c_title, c_url, c_keys)),
                   columns=['Role', 'State', 'Until', 'Title', 'URL', 'Keys'])
    return df


if __name__ == "__main__":

    config = load_configs('../config/app.cfg')
    URL_BASE = str(config['SCRAPING']['URL_BASE'])
    HEADERS  = str(config['SCRAPING']['HEADERS'])
    keywords = config['FIND']['keywords'].split(',')

    response = requests.get(URL_BASE, headers={'User-Agent': HEADERS})
    soup = BeautifulSoup(response.content, "html.parser")

    df = create_df(soup, keywords)
    df.to_csv('../output/contest_out.csv', index=False)

