''' ETL Objects '''

from ..bot import telegram

class PCIContest(telegram.TBot):

    def __init__(self):
        super().__init__()
        self.load_cfg()
        self.load_df()

    def load_cfg(self):
        self.config.url = str(self.cfg['PCI']['url_base'])
        self.config.headers = str(self.cfg['PCI']['headers'])
        self.config.output = str(self.cfg['PCI']['output'])
        self.config.keywords = self.cfg['GERAL']['keywords'].split(',')

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
        c_keys, c_txt_body = self.check_keywords(c_url)
        self.df.drop(self.df.index, inplace=True)
        self.df.drop(self.df.columns, inplace=True, axis=1)
        self.df[self.config.fields] = list(zip(c_role, c_state, c_until,
                                               c_title, c_url, c_keys, c_txt_body))
        self.df.fillna('', inplace=True)

    def check_keywords(self, url_list):
        c_keys, c_txt_body = [], []
        for url in url_list:
            self.logger.info("%s", url.split('/')[-1])
            _, body_soup = self.extract_page_html(url)
            txt_body = self.r_tags(body_soup.find("div", {"itemprop": "articleBody"})).lower()
            c_txt_body.append(txt_body)
            keys = ''
            for key in self.config.keywords:
                if key in txt_body:
                    keys = keys + key + ', '
            c_keys.append(keys[:-2])
        return c_keys, c_txt_body
