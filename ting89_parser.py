import os
import logging
import re
from typing import List
import argparse
import requests
from bs4 import BeautifulSoup


def add_arg(parser):
    parser.add_argument("url", help="specify the ting89 url")
    parser.add_argument("-n", "--no-download", help="only print the downloaded mp3 files", dest="no_download",
                        action="store_true")
    parser.add_argument("--no-folder", help="don't create folder", dest="no_folder", action="store_true")


def find_title(soup):
    return str(soup.find_all("h1")[0].contents[0])


def soup_find_mp3_link(soup):
    result = soup.find_all("iframe")
    return re.search(".*url=(.*mp3)", str(result[0])).group(1)


def get_mp3_links(url: str):
    """get list of mp3 links from ting89 url"""
    ret = requests.get(url)
    ret.encoding = "GBK"
    html_text = ret.text
    soup = BeautifulSoup(html_text, 'html.parser')
    title = find_title(soup)
    logging.info("found title to be: " + title)
    mp3_links = []
    for filtered_tags in (filter(lambda _x: "href=\"/down" in str(_x), soup.find_all("li"))):
        mp3_url = "http://www.ting89.com" + str(filtered_tags.a["href"])
        logging.info(f"getting mp3 download link : {mp3_url}")
        r = requests.get(mp3_url)
        r.encoding = "GBK"
        soup = BeautifulSoup(r.text, "html.parser")
        mp3_links.append(soup_find_mp3_link(soup))
    return title, mp3_links


def download(title: str, mp3_lists: List[str], config=None):
    prefix = ""
    if not config.no_folder:
        if not os.path.exists(title):
            os.mkdir(title)
        prefix = title + "/"
    for i, mp3_url in enumerate(mp3_lists):
        file_output = "{}_{}.mp3".format(title, i)
        logging.info(f"downloading {file_output} at {mp3_url}")
        if not config.no_download:
            r = requests.get(mp3_url)
            open(f"{prefix}{file_output}", "wb").write(r.content)
            logging.info(f"successfully downloaded {file_output}")
        else:
            logging.info("Download skipped.")


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    add_arg(parser)
    args = parser.parse_args()
    title, complete_url_list = get_mp3_links(args.url)
    download(title, complete_url_list, args)


if __name__ == '__main__':
    main()
