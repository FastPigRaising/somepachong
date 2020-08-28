import requests,xlwt,time
from bs4 import BeautifulSoup
import multiprocessing

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Referer' : 'https://movie.douban.com/top250'
}

book = xlwt.Workbook(encoding='utf-8',style_compression=0)

sheet = book.add_sheet('豆瓣250',cell_overwrite_ok=True)
sheet.write(0,0,'名称')
sheet.write(0,1,'排名')
sheet.write(0,2,'评分')
sheet.write(0,3,'作者')
sheet.write(0,4,'简介')
sheet.write(0,5,'图片')

n =1

def main(url):
    html = request_douban(url)
    soup = BeautifulSoup(html,'lxml')
    save_to_excel(soup)

# 获取网页信息
def request_douban(url):
    try:
        req = requests.get(url,headers=headers)
        if req.status_code == 200:
            return req.text
    except requests.RequestException:
        return None

# 储存数据
def save_to_excel(soup):
    moive_list = soup.find(class_='grid_view').find_all('li')
    # print(moive_list)

    for item in moive_list:
        item_name = item.find(class_='title').string
        item_img = item.find('a').find('img').get('src')
        item_index = item.find(class_='').string
        item_score = item.find(class_='rating_num').string
        item_auther = item.find('p').text.strip()
        if item.find(class_='inq') != None:
            item_intr = item.find(class_='inq').string
        else:
            item_intr = None

        # print('获得电影数据'+'|'+item_index+'|'+ item_name +'|'+item_intr+'|'+item_auther)
        global n
        sheet.write(n, 0, item_name)
        sheet.write(n, 1, item_index)
        sheet.write(n, 2, item_score)
        sheet.write(n, 3, item_auther)
        sheet.write(n, 4, item_intr)
        sheet.write(n, 5, item_img)
        n +=1


if __name__ == '__main__':
    start = time.time()
    urls =[]
    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    for i in range(0,10):
        url = 'https://movie.douban.com/top250?start=' + str(i * 25) + '&filter='
        urls.append(url)
    pool.map(main,urls)
    pool.close()
    pool.join()
    book.save(u'豆瓣排名前250电影1.xlsx')