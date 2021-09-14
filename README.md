# Contest BotScraper

[![Pylint](https://github.com/jefersonjlima/pci_scraper/actions/workflows/pylint.yml/badge.svg)](https://github.com/jefersonjlima/pci_scraper/actions/workflows/pylint.yml)
[![Ubuntu](https://github.com/jefersonjlima/pci_scraper/actions/workflows/Ubuntu.yml/badge.svg)](https://github.com/jefersonjlima/pci_scraper/actions/workflows/Ubuntu.yml)
![GitHub](https://img.shields.io/github/license/jefersonjlima/pci_scraper)


## Overview

Contest BotScrapy is a web crawling, used to crawl Brazilian contests websites and extract structured data from their pages.

Check the BotScrapy homepage at [BotScraper](http://github.io/jefersonjlima/pci_scraper) for more information, including a list of features.

## Requirements

* Python 3.7+
* Tested on Linux (Ubuntu).


## Install

The quick way:

```bash
$ git clone https://github.com/jefersonjlima/botscraper.git
$ cd botscraper && mkdir output
$ echo 'export TELEGRAM_TOKEN="YOUR_ACCESS_TOKEN"' >> ~/.bashrc
$ make prepare-dev
$ make run
```

## Configuration

First of all, if you want to use the botscraper with telegram, you will need an Access Token. The lazy way to generate a Telegram Token is you have to talk to [@BotFather](https://telegram.me/botfather) and follow a few simple steps to generate it.

Edit the `config/configs.cfg` to change the configurations.
For example, if you want to add or remove some keyword you need to change `GERAL.keywords` (you can do it by the telegram commands too). If you are looking for an internship, just change the `url_base` to `https://www.pciconcursos.com.br/estagios/`.

In `TELEGRAM.etl_schedule` you will define the UTC time to start the ETL.

## Commands
* `/help`to see all commands.
* `/set <keyword>` to add new keyword.
* `/unset <keyword>` to remove a keyword.
* `/notify` to enable notification.
* `/non_notify` to disable notification.
* `/keywords` to show all keywords.
* `/show <keyword>` to list costests by keyword.
* `/show to show all filtered contests.

## Documentation

Documentation is available online at [BotScraper](http://github.io/jefersonjlima/pci_scraper) and in the `docs` directory.


## Contributing
