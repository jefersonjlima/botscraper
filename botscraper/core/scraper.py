''' BotScraper Object '''

import ast
import logging
import configparser
from dataclasses import dataclass, field
from datetime import datetime
import re
from bs4 import BeautifulSoup
import pandas as pd
import requests

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

@dataclass
class Config:
    url: str = ''
    headers: str = ''
    output: str = ''
    drops: dict = field(default_factory=dict)
    keywords: list = field(default_factory=list)
    fields: list = field(default_factory=list)
    alarm: list = field(default_factory=list)


class ETL:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.soup = None
        self.config = Config()
        self.load_cfg_file('config/configs.cfg')
        self.config.fields = self.cfg['DATABASE']['fields'].split(',')
        self.config.drops = ast.literal_eval(self.cfg['DATABASE']['drops'])
        self.df = pd.DataFrame()
        self.last_df = None
        self.c_news = []

    def load_cfg_file(self, cfg_path) -> None:
        self.cfg = configparser.ConfigParser()
        self.cfg.read(cfg_path)

    def load_df(self) -> None:
        try:
            self.last_df = pd.read_csv(self.config.output)
            self.last_df.fillna('', inplace=True)
        except IOError:
            self.logger.error("Error to load last_df")

    def news_df(self):
        try:
            df_tmp = self.df[self.df['Keys'] != '']
            df_url = df_tmp['URL'].drop_duplicates()
            last_df_tmp = self.last_df[self.last_df['Keys'] != '']
            last_df_url = last_df_tmp['URL'].drop_duplicates()
            self.c_news = list(set(df_url) - set(last_df_url))
        except KeyError:
            self.logger.error("Please, make sure if ETL.run was called")

    def drops_df(self):
        for key in self.config.drops:
            self.df = self.df[~self.df[key].str.contains(
                self.config.drops[key])]

    def create_df(self):
        pass

    def extract_page_html(self, url) -> (bool, BeautifulSoup):
        response = requests.get(url, headers={'User-Agent': self.config.headers})
        soup = BeautifulSoup(response.content, 'html.parser')
        return response.ok, soup

    @staticmethod
    def r_tags(element) -> str:
        remove_tags = re.compile(r'<[^>]+>')
        out = remove_tags.sub('', str(element))
        out = out.replace('\n', '')
        out = out.replace(';', '')
        return out

    def try_date(self, date_str) -> str:
        format_str = '%d/%m/%Y'
        try:
            out = datetime.strptime(date_str, format_str)
        except ValueError:
            self.logger.error("Datetime error!")
            out = datetime.fromtimestamp(0).strftime(format_str)
        return out

    def storage(self) -> None:
        try:
            self.df.to_csv(self.config.output, index=False)
        except  IOError:
            self.logger.error("Error to Storage!")

    def run(self) -> None:
        # Extract
        _, self.soup = self.extract_page_html(self.config.url)
        # Transform
        self.create_df()    # create database
        self.drops_df()     # drop values
        self.news_df()      # get news
        # Load
        self.storage()      # storage database
        self.load_df()      # update values
