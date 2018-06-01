import requests
from bs4 import BeautifulSoup

def search_webtoon(keyword):
    params = {'keyword': keyword}
    response = requests.get('https://comic.naver.com/search.nhn?', params)
    soup = BeautifulSoup(response.text, 'lxml')
    result_list = soup.select('ul.resultList > li')

    search_list = list()
    for index, result in enumerate(result_list):
        try:

            if result.select_one('img').get('title').strip() == '웹툰':
                search_list.append(result.select_one('img').find_next_sibling().contents[0])
        except AttributeError:
            break

    if search_input:
        for index, i in enumerate(search_list):
            print(f'{index+1}.', i)
    else:
        print('검색 결과가 없습니다. 다른 검색어를 입력해주세요')



if __name__ == '__main__':
    print('안내) Ctrl+C로 종료합니다.')
    search_input = input('검색할 웹툰명을 입력해주세요 : ')
    search_webtoon(search_input)
    choice_input = input('선택 : ')