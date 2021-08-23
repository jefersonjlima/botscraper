''' ETL Objects '''

from datetime import datetime
from dataclasses import dataclass
from ..core import Scraper


class PCIContest(Scraper.ETL):

    def __init__(self):
        super().__init__()
        self.load_page()

    def load_page(self):
        self.config.URL = str(self.cfg['PCI']['URL_BASE'])
        self.config.HEADERS = str(self.cfg['PCI']['HEADERS'])
        self.config.keywords = tuple(self.cfg['GERAL']['keywords'].split(','))

    def create_df(self):
        contests = self.soup.find_all("div", attrs={"class": "ca"})
        c_role, c_state, c_until, c_title, c_url = [], [], [], [], []
        for cnt in contests:
            c_role.append(self.r_tags(str(cnt.select_one('span')).rsplit('br')[0][:-1]))
            c_state.append(self.r_tags(cnt.select('div')[1]))
            date_str = self.try_date(self.r_tags(cnt.select('div')[3])[-10:])
            c_until.append(date_str)
            c_title.append(cnt.select('a')[0].get('title'))
            c_url.append(cnt.select('a')[0].get('href'))
        c_keys = self.check_keywords(c_url)
        self.df[self.config.FIELDS] = list(zip(c_role, c_state, c_until, c_title, c_url, c_keys))

    def check_keywords(self, url_list):
        c_keys = []
        for url in url_list:
            print(f"Checking keywords in: {url}")
            s = self.extract_page_html(url)
            txt_body = self.r_tags(s.find("div", {"itemprop": "articleBody"})).lower()
            keys = ''
            for key in self.config.keywords:
                if key in txt_body:
                    keys= keys + key + ' '
            c_keys.append(keys)
            print(keys)
        return c_keys

