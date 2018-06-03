import os
from urllib import parse

import requests
from bs4 import BeautifulSoup


class Webtoon:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        self.title = None
        self.author = None
        self.description = None
        self.no = None
        self.num_of_episodes = None
        self.episode_list = list()
        self.html =  ''
        self.number_pages = None

    def get_html(self, number_page=None):
        if number_page is None:
            number_page = 1

        # print(f'get_html함수가 실행됨..페이지{number_page}', self.webtoon_id)
        file_path = f'data/webtoon-{self.webtoon_id}-{number_page}.html'
        address = 'https://comic.naver.com/webtoon/list.nhn?'
        params = {
            'titleId': self.webtoon_id,
            'page':number_page,
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
        # print(f'set_info가 실행됨')
        html = self.html
        soup = BeautifulSoup(html, 'lxml')
        div_detail = soup.select_one('div.detail')
        self.title = div_detail.select_one('h2').contents[0].strip()
        self.author = div_detail.select_one('h2 > span.wrt_nm').contents[0].strip()
        self.description = div_detail.select_one('p').get_text(strip=True, separator='\n')
        self.number_pages = soup.select('div.page_wrap > a.page')[-1].get_text()

        html = self.html
        soup = BeautifulSoup(html, 'lxml')
        tr_list = soup.select_one('table.viewList').select('tr')
        episode_list = list()
        for index, tr in enumerate(tr_list[1:]):
            if tr.get('class'):
                continue
            from urllib import parse
            url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
            query_string = parse.urlsplit(url_detail).query
            query_dict = parse.parse_qs(query_string)
            self.no = query_dict['no'][0]
            episode_list.append(self.no)

        self.num_of_episodes = episode_list[0]


    def crawl_episode_list(self):

        episode_list = list()
        for number in range(1, int(self.number_pages)+1):
            self.get_html(number)
            soup = BeautifulSoup(self.html, 'lxml')
            table = soup.select_one('table.viewList')
            tr_list = table.select('tr')
            for index, tr in enumerate(tr_list[1:]):
                if tr.get('class'):
                    continue
                url_detail = 'https://comic.naver.com'+tr.select_one('td:nth-of-type(1) > a').get('href')
                title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
                from urllib import parse
                query_string = parse.urlsplit(url_detail).query
                query_dict = parse.parse_qs(query_string)
                episode_no = query_dict['no'][0]
                new_episode = Episode(
                    webtoon=self,
                    title = title,
                    url = url_detail,
                    episode_no = episode_no
                )
                episode_list.append(new_episode)
        return episode_list


class Episode:
    def __init__(self, webtoon, title, url, episode_no):
        self.webtoon = webtoon
        self.title = title
        self.url = url
        self.episode_no = episode_no

    def __repr__(self):
        return f'{self.title}'

    def get_image_url_list(self):
        file_path = 'data/episode_detail-{webtoon_id}-{episode_no}.html'.format(
            webtoon_id=self.webtoon.webtoon_id,
            episode_no=self.episode_no,
        )
        # print('file_path:', file_path)
        # print(self.url)
        # 위 파일이 있는지 검사
        if os.path.exists(file_path):
            # print('os.path.exists: True')
            # 있다면 읽어온 결과를 html변수에 할당
            html = open(file_path, 'rt').read()
        else:
            # 없다면 self.url에 requests를 사용해서 요청
            #  요청의 결과를 html변수에 할당
            #  요청의 결과를 file_path에 해당하는 파일에 기록
            # print('os.path.exists: False')
            # print(' http get request, url:', self.url)
            response = requests.get(self.url)
            html = response.text
            open(file_path, 'wt').write(html)
        soup = BeautifulSoup(html, 'lxml')
        img_list = soup.select('div.wt_viewer > img')

        # episode_image = EpisodeImage(self.webtoon, self.title, img_list)

        return [img.get('src') for img in img_list]


    def download_all_images(self):
        for url in self.get_image_url_list():
            self.download(url)
        print(f'{self} 저장 완료')

    def download(self, url_img):
        """
        :param url_img: 실제 이미지의 URL
        :return:
        """
        # 서버에서 거부하지 않도록 HTTP헤더 중 'Referer'항목을 채워서 요청
        url_referer = f'http://comic.naver.com/webtoon/list.nhn?titleId={self.webtoon.webtoon_id}'
        headers = {
            'Referer': url_referer,
        }
        response = requests.get(url_img, headers=headers)

        # 이미지 URL에서 이미지명을 가져옴
        file_name = url_img.rsplit('/', 1)[-1]

        # 이미지가 저장될 폴더 경로, 폴더가 없으면 생성해준다
        dir_path = f'data/{self.webtoon.webtoon_id}/{self.episode_no}'
        os.makedirs(dir_path, exist_ok=True)

        # 이미지가 저장될 파일 경로, 'wb'모드로 열어 이진데이터를 기록한다
        file_path = f'{dir_path}/{file_name}'
        open(file_path, 'wb').write(response.content)


class EpisodeImage:
    def __init__(self, webtoon, episode, url):
        self.webtoon = webtoon
        self.episode = episode
        self.url = url
        self.file_path = None

    def set_episode_images(self):
        return



webtoon1 = Webtoon(632342)
webtoon1.get_html()
webtoon1.set_info()
webtoon1.crawl_episode_list()







