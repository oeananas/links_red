import json
import requests
import os
from dotenv import load_dotenv
import argparse


def add_short_link(long_url, token):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    params = {
        'long_url': long_url
    }
    res = requests.post(url=url, json=params, headers=headers)
    if res.ok:
        return res.json()


def get_summ_clicks(bitlink, token):
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(bitlink)
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    res = requests.get(url=url, headers=headers)
    if res.ok:
        return res.json()


def check_is_bitlink(link, token):
    link = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(link)
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    return requests.get(url=link, headers=headers).ok


if '__main__' == __name__:
    load_dotenv()
    parser = argparse.ArgumentParser(
        description='Сокращение ссылок при помощи API bitly'
    )
    parser.add_argument('link', help='ссылка на страницу')
    args = parser.parse_args()
    url = args.link
    token = os.getenv("TOKEN")
    if check_is_bitlink(url, token):
        summ_clicks = get_summ_clicks(bitlink=url, token=token)
        if summ_clicks:
            print('Количество переходов по ссылке bitly: {}'.format(summ_clicks['total_clicks']))
        else:
            exit('invalid url')
    else:
        short_link = add_short_link(long_url=url, token=token)
        if short_link:
            print('Сокращенная ссылка: {}'.format(short_link['id']))
        else:
            exit('invalid url')
