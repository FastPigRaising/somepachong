import re,requests,json,time


# http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-1
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Referer' : 'http://bang.dangdang.com/books/fivestars'
}

#  主函数
def main(page):
    url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-' + str(page)
    html = request_dandan(url)
    # print(html)
    items = parse_result(html)
    for item in items:
        # print(item)
        save(item)

#  获取网页信息
def request_dandan(url):
    try:
        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            return req.text
    except requests.RequestException:
        return None


# 解析网页
def parse_result(html):
    pattern = re.compile('<li>.*?list_num.*?(\d+).</div>.*?<img src="(.*?)" alt="(.*?)".*?<span class="tuijian">(.*?)</span>.*?<div class="publisher_info">.*?target="_blank">(.*?)</a>.*?<div class="publisher_info"><span>(.*?)</span>&nbsp.*?<span class="price_n">&yen;(.*?)</span>.*?</li>',re.S)
    items = re.findall(pattern,html)
    print(items)
    for item in items:
        yield {
            'range' : item[0],
            'img' : item[1],
            'name' : item[2],
            'recomend' : item[3],
            'author' : item[4],
            'price' : item[5]
        }
    return items


# 存储信息
def save(item):
    print('开始写入数据===》',item)
    with open('book.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(item,ensure_ascii=False) + '\n')
        f.close()

if __name__ == '__main__':
    for i in range(1,26):
        main(1)
        time.sleep(1)
    print('end')