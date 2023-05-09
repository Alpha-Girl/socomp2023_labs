from datetime import date
from lxml import etree
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options() # 实例化Option对象
chrome_options.add_argument('--headless') # 把Chrome浏览器设置为静默模式
chrome_options.add_argument('--disable-gpu') # 禁止加载图片
driver=webdriver.Edge()
# driver = webdriver.Chrome(options = chrome_options) # 设置引擎为Chrome，在后台默默运行

url = 'http://www.pbc.gov.cn/huobijinyinju/147948/147964/index.html'


def driver_url():
    driver.get(url)
    html = etree.HTML(driver.page_source)
    return html


def check_date(html):
    today = str(date.today())
    extract_announcements_list = html.xpath('//*[@id="22786"]/div[2]/div[1]/table/tbody/tr[2]/td/table')
    for i in extract_announcements_list:
        announcement_date = i.xpath('./tbody/tr/td[2]/span/text()')
        if today == announcement_date[0]:
            announcement_title = i.xpath('./tbody/tr/td[2]/font/a/@title')
            announcement_link = i.xpath('./tbody/tr/td[2]/font/a/@href')
            real_link = 'http://www.pbc.gov.cn'+announcement_link[0]
            print_announcement(announcement_title,real_link)
        else:
            print('No %s new announcement.'%today)
            sys.exit()


def print_announcement(title, link):
    print(title, end=' ')
    print(link)


if __name__ == '__main__':
    res_html = driver_url()
    print(res_html)
    check_date(res_html)
