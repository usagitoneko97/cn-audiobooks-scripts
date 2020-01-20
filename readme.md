## various chinese audiobooks site scraper

Script that downloads all episodes from the audiobook site without having to manually download each one of them. 
This script is hacked together within 1 hour. Use it on your own discretion.

Currently supported: 
- ting89.com

## installation requirement
This script required python requests and beautifulsoup4

## usage
```
usage: ting89_parser.py [-h] [-n] [--no-folder] url

positional arguments:
  url                specify the ting89 url

optional arguments:
  -h, --help         show this help message and exit
  -n, --no-download  only print the downloaded mp3 files
  --no-folder        don't create folder
```