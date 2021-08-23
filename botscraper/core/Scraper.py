# BotScraper Object

import configparser
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from datetime import datetime
import pandas as pd
import requests
import re


@dataclass
class Config:
    URL     : str = ''
    HEADERS : str = ''
    keywords: tuple = ()
    fields  : list = field(default_factory=list)


class ETL:

    def __init__(self):
        self.soup = None
        self.config = Config()
        self.load_cfg_file('config/configs.cfg')
        self.config.FIELDS = self.cfg['DATABASE']['FIELDS'].split(',')
#        self.df = pd.DataFrame(columns=self.config.FIELDS)
        self.df = pd.DataFrame()

    def load_cfg_file(self, cfg_path):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(cfg_path)

    def extract_page_html(self, url):
        response = requests.get(url,
                headers={'User-Agent': self.config.HEADERS})
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    @staticmethod
    def r_tags(element):
        remove_tags = re.compile(r'<[^>]+>')
        out = remove_tags.sub('', str(element))
        out = out.replace('\n', '')
        out = out.replace(';', '')
        return out

    @staticmethod
    def try_date(date_str):
        format_str = '%d/%m/%Y'
        try:
            out = datetime.strptime(date_str, format_str)
        except:
            out = datetime.fromtimestamp(0).strftime(format_str)
        return out

    def storage(self):
        # TODO Database?
        try:
            self.df.to_csv('output/contest_out.csv', index=False)
        except:
            print("Error to Storage!")

    def run(self):
        # Extract
        self.soup = self.extract_page_html(self.config.URL)
        # Transform
        self.create_df()
        # Load
        self.storage()





