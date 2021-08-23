from setuptools import setup


with open('requirements.txt', 'rt') as f:
    requirements_list = [req[:-1] for req in f.readlines()]

setup(
    name='botscraper',
    version='0.0.1',
    packages=['botscraper', 'botscraper.core', 'botscraper.scrapers'],
    url='https://github.com/jefersonjlima/pci_scraper',
    license='MIT',
    author='Jeferson Lima',
    author_email='jefersonjl82@gmail.com',
    description='BotScraper: A Contests BotScraper',
    install_requires = requirements_list)
