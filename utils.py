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
        file_path = f'data/webtoon-{self.webtoon_id}.html'
        address = 'https://comic.naver.com/webtoon/list.nhn?titleId=651673&weekday=wed'
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



# if __name__ == '__main__':
#     webtoon1 = Webtoon(651673)
#     webtoon1.get_html()
#     # print(webtoon1.html)
#     print(webtoon1.set_info())