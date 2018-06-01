import os
import requests
from bs4 import BeautifulSoup


class Webtoon:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        self.title = None
        self.author = None
        self.description = None
        self.episode_list = list()
        self.html =  ''

    def get_html(self):
        print('get_html함수가 실행됨..', self.webtoon_id)
        file_path = f'data/webtoon-{self.webtoon_id}.html'
        address = 'https://comic.naver.com/webtoon/list.nhn?'
        params = {
            'titleId': self.webtoon_id
        }
        if os.path.exists(file_path):
            html = open(file_path, 'rt').read()
        else:
            response = requests.get(address, params)
            html = response.text
            open(file_path, 'wt').write(html)
        self.html = html
        return self.html

    def set_info(self):
        html = self.html
        soup = BeautifulSoup(html, 'lxml')
        div_detail = soup.select_one('div.detail')
        self.title = div_detail.select_one('h2').contents[0].strip()
        self.author = div_detail.select_one('h2 > span.wrt_nm').contents[0].strip()
        self.description = div_detail.select_one('p').contents[0].strip()


class Episode:
    def __init__(self, webtoon):
        self.webtoon = webtoon
        self.title = None
        self.url = None

class EpisodeImage:
    def __init__(self):
        self.episode = None
        self.url = None
        self.file_path = None


