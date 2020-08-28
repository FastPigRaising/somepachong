from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import xlwt,time

browser = webdriver.PhantomJS()
# browser = webdriver.Chrome()
WAIT = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)

book = xlwt.Workbook(encoding='utf-8',style_compression=0)

sheet = book.add_sheet('龙王',cell_overwrite_ok=True)
sheet.write(0, 0, '名称')
sheet.write(0, 1, '地址')
sheet.write(0, 2, '描述')
sheet.write(0, 3, '观看次数')
sheet.write(0, 4, '弹幕数')
sheet.write(0, 5, '发布时间')

n = 1

def search():
    try:
        print('--开始访问B站--')
        browser.get("https://www.bilibili.com/")
        input = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nav_searchform > input")))
        submit = WAIT.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div/form/div/button')))

        input.send_keys('歪嘴龙王')
        submit.click()

        print('跳转到新的窗口')
        all_h = browser.window_handles
        browser.switch_to.window(all_h[1])
        get_source()

        total = WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.last > button")))
        return int(total.text)

    except TimeoutException:
        return search()

def next_page(page_num):
    try:
        print('获取下一页信息')
        next_btn = WAIT.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.next > button')))
        next_btn.click()
        WAIT.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#all-list > div.flow-loader > div.page-wrap > div > ul > li.page-item.active > button'),str(page_num)))

        get_source()
    except TimeoutException:
        browser.refresh()
        return next_page(page_num)


def save_to_excel(soup):
    vedio_list =  soup.find(class_='video-list clearfix').find_all(class_='video-item matrix')

    for item in vedio_list:
        item_title = item.find('a').get('title')
        item_link = item.find('a').get('href')
        item_dec = item.find(class_='des hide').text
        item_view = item.find(class_='so-icon watch-num').text
        item_biubiu = item.find(class_='so-icon hide').text
        item_date = item.find(class_='so-icon time').text

        print('爬取' + item_title)

        global n

        sheet.write(n, 0, item_title)
        sheet.write(n, 1, item_link)
        sheet.write(n, 2, item_dec)
        sheet.write(n, 3, item_view)
        sheet.write(n, 4, item_biubiu)
        sheet.write(n, 5, item_date)

        n += 1

def get_source():
    WAIT.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#all-list > div.flow-loader > div.filter-wrap')))
    html = browser.page_source
    soup = BeautifulSoup(html,'lxml')
    save_to_excel(soup)

def main():
    try:
        total = search()
        print(total)

        for i in range(2,int(total+1)):
            next_page(i)
            time.sleep(1)
            if i >= 20:
                break

    finally:
        browser.close()

if __name__ == '__main__':
    main()
    book.save('歪嘴龙王.xlsx')



'''
<li class="video-item matrix">
<a href="//www.bilibili.com/video/BV11T4y177Ps?from=search" title="老网抑云用户了" target="_blank" class="img-anchor">
    <div class="img">
        <div class="lazy-img">
            <img alt="" src="">
        </div>
        <span class="so-imgTag_rb">02:23
        </span>
        <div class="watch-later-trigger watch-later">
        </div>
        <span class="mask-video">
        </span>
    </div>
    <!---->
</a>

<div class="info">
    <div class="headline clearfix">
        <!---->
        <!---->
        <span class="type hide">搞笑
        </span>
        <a title="老网抑云用户了" href="//www.bilibili.com/video/BV11T4y177Ps?from=search" target="_blank" class="title">老
            <em class="keyword">网抑云
            </em>用户了
        </a>
    </div>
    <div class="des hide">
        看你这样子，老网抑云了吧
        素材来源于网络
        音乐：KripMus Rido - Я тебя теряю 2
    </div>
    <div class="tags">
        <span title="观看" class="so-icon watch-num">
            <i class="icon-playtime">
            </i>
            236.5万
        </span>
        <span title="弹幕" class="so-icon hide">
            <i class="icon-subtitle">
            </i>
            1668
        </span>
        <span title="上传时间" class="so-icon time">
            <i class="icon-date">
            </i>
            2020-07-04
        </span>
        <span title="up主" class="so-icon">
            <i class="icon-uper">
            </i>
            <a href="//space.bilibili.com/313950018?from=search" target="_blank" class="up-name">颜明主
            </a>
        </span>
    </div>
</div>
</li>
'''


