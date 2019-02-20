from time import sleep

import requests
from bs4 import BeautifulSoup


def data_wrapper(data, **kwargs):
    """for debug"""
    for i, v in kwargs.items():
        data[i] = v


def get_soup(url, interval=0.25):
    res = requests.get(url)
    sleep(interval)
    res.encoding = res.apparent_encoding
    return BeautifulSoup(res.content, 'lxml')
