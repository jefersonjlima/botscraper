# BotScraper Object

import configparser
from dataclasses import dataclass, field
from datetime import datetime
import re
from bs4 import BeautifulSoup
import pandas as pd
import requests


@dataclass
class Config:
    url: str = ''
    headers: str = ''
    keywords: tuple = ()
    fields: list = field(default_factory=list)


class ETL:

    def __init__(self):
        self.soup = None
        self.config = Config()
        self.load_cfg_file('config/configs.cfg')
        self.config.fields = self.cfg['DATABASE']['FIELDS'].split(',')
        self.df = pd.DataFrame()

    def load_cfg_file(self, cfg_path):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(cfg_path)

    def extract_page_html(self, url):
        response = requests.get(url, headers={'User-Agent': self.config.headers})
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
        except ValueError as e:
            print(f"Datetime error: {e}")
            out = datetime.fromtimestamp(0).strftime(format_str)
        return out

    def create_df(self) -> None:
        pass

    def load_page(self) -> None:
        pass

    def storage(self):
        try:
            self.df.to_csv('output/contest_out.csv', index=False)
        except  IOError as e:
            print(f"Error to Storage: {e}")

    def run(self):
        # Extract
        self.soup = self.extract_page_html(self.config.url)
        # Transform
        self.create_df()
        # Load
        self.storage()
