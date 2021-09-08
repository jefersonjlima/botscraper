""" ETL Test """

import pytest
from botscraper import PCIContest
import botscraper

def test_loag_cfg_file():
    etl = PCIContest()
    assert etl.cfg['GERAL']['VERSION'] == botscraper.__version__

def test_extract_page():
    etl = PCIContest()
    r, _ = etl.extract_page_html(etl.config.url)
    assert r == True

