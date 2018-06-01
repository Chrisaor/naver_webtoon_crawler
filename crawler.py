from itertools import count
import requests
from bs4 import BeautifulSoup
from utils import Webtoon, Episode, EpisodeImage

class SearchWebtoon:
    def __init__(self):
        self.search_list = None
        self.webtoon_id_list = None

    def search_webtoon(self, keyword):
        params = {'keyword': keyword}
        response = requests.get('https://comic.naver.com/search.nhn?', params)
        soup = BeautifulSoup(response.text, 'lxml')
        result_list = soup.select('ul.resultList > li')

        search_list = list()
        webtoon_id_list = list()
        for index, result in enumerate(result_list):
            try:
                if result.select_one('img').get('title').strip() == '웹툰':
                    search_list.append(result.select_one('img').find_next_sibling().contents[0])
                    webtoon_id_list.append(result.select_one('h5').a['href'].split('=')[-1])
                self.search_list = search_list
                self.webtoon_id_list = webtoon_id_list
            except AttributeError:
                break

        if search_list:
            for index, title, number in zip(count(),search_list, webtoon_id_list):
                print(f'{index+1}. {title} [{number}]')


        else:
            print('검색 결과가 없습니다. 다른 검색어를 입력해주세요')
            search_input = input('검색할 웹툰명을 입력해주세요 : ')
            return self.search_webtoon(search_input)


if __name__ == '__main__':
    print('안내) Ctrl+C로 종료합니다.')
    search_input = input('검색할 웹툰명을 입력해주세요 : ')
    webtoon = SearchWebtoon()
    webtoon.search_webtoon(search_input)
    choice_input = input('선택 : ')

