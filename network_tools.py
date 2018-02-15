# coding: utf-8

import http.client
import re
import urllib.error
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import sys
from bs4 import BeautifulSoup as Bs

__author__ = 'isac322'


def down_file(judge_id, cookie):
    header = {
        'Host': 'www.acmicpc.net',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Origin': 'https://www.acmicpc.net,.',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/45.0.2454.101 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://www.acmicpc.net/source/{}'.format(judge_id),
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cookie': cookie + ' _gauges_unique_day=1; _gauges_unique_month=1; _gauges_unique_year=1; _gauges_unique=1; '
                           '_ga=GA1.2.1918118912.1444272664'
    }

    conn = http.client.HTTPSConnection('www.acmicpc.net')
    conn.request('POST', '/source/download/{}'.format(judge_id), None, header)

    response = conn.getresponse()
    code = response.read()

    response.close()

    return code


def login(user_name, pw):
    query = {'login_user_id': user_name, 'login_password': pw}
    data = urlencode(query)
    header = {
        'Host': 'www.acmicpc.net',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Origin': 'https://www.acmicpc.net',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/45.0.2454.101 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://www.acmicpc.net/login/?next=/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
    }

    conn = http.client.HTTPSConnection('www.acmicpc.net')
    conn.request('POST', '/signin', data, header)
    response = conn.getresponse()

    if 'error' in response.info()['Location']:
        print('invalid login')
        exit(1)

    cookie = ''
    patt = re.compile('^.*((__cfduid|OnlineJudge|acmicpcautologin)[=][\w\d]+;).*$', re.MULTILINE)

    for line in patt.finditer(str(response.info())):
        cookie += line.group(1) + ' '

    response.close()
    # print(response.msg)

    return cookie


def get_soup(url, query=None):
    response = get_response(url, query)
    ret = Bs(response, 'html.parser')
    response.close()
    return ret


def get_response(url, query=None, header=None):
    if header is None:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/45.0.2454.101 Safari/537.36'
        header = {
            'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': user_agent,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    data = None
    if query is not None:
        data = urlencode(query).encode('utf-8')

    req = Request(url, data, header)

    try:
        response = urlopen(req)
        return response

    except urllib.error.HTTPError:
        print('invalid username')
        sys.exit(1)


if __name__ == '__main__':
    print('please run main.py')
