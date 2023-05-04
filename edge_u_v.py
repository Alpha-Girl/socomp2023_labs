from datetime import date
from lxml import etree
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import pymongo
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge

edge_options = EdgeOptions()
# edge_options.use_chromium = True
# 设置无界面模式，也可以添加其它设置
edge_options.add_argument('headless')
# driver = Edge(options=edge_options)
# r = driver.get('https://www.baidu.com')
edge_options.binary_location="C:/Users/dell/Desktop/MicrosoftWebDriver.exe"
chrome_options = Options() # 实例化Option对象
chrome_options.add_argument('headless') # 把Chrome浏览器设置为静默模式
# chrome_options.add_argument('disable-gpu') # 禁止加载图片
driver=webdriver.Edge("C:/Users/dell/Desktop/MicrosoftWebDriver.exe")
# driver = webdriver.Chrome(options = chrome_options) # 设置引擎为Chrome，在后台默默运行
import csv
url = 'https://www.congress.gov/search?q=%7B%22source%22%3A%22members%22%2C%22search%22%3A%22O000167%22%7D'


def driver_url(id,meet,db):
    url="https://www.congress.gov/search?q=%7B%22source%22%3A%22members%22%2C%22search%22%3A%22"+id+"%22%7D"
    driver.get(url)
    # driver.print_page()
    # driver.get_pinned_scripts()
    # print(driver.find_element(value="Party"))
    t=driver.page_source
    t=t.replace("\n","")
    D1=re.findall(r"<span>D(.+?)c</span>",t)
    # print(re.findall(r"<span>R(.+?)n</span>",t))
    R1=re.findall(r"<span>R(.+?)n</span>",t)

    # print(re.findall(r"<span>I(.+?)t</span>",t))
    I1=re.findall(r"<span>In(.+?)t</span>",t)
    if len(D1)>1:
        party="Democratic"
    elif len(R1)>1:
        party="Republican"
    elif len(I1)>1:
        party="In"+I1[0]+"t"
    else:
        party="Unknown"
    # print(party)
    x=re.findall(r"<div class=\"member-image\"><img src=\"/img/member/(.+?)></div>",t)
    x=x[0]
    x=re.findall(r"alt=\"(.+?)\"",x)
    x=x[0]
    # ppp=re.compile(r"<strong>State:</strong><span>(.+?)</span>",re.M)
    # state=ppp.match(t)
    t=t.replace(" ","")
    
    state=re.findall(r"<strong>State:</strong><span>(.+?)</span>",t)
    if state==[]:
        state=["Unknown"]
    state=state[0]
    serve=re.findall(r"<ulclass=\"member-served\">(.+?)</ul>",t)
    if serve==[]:
        serve=["Unknown"]
    serve=serve[0].replace("</li><li>"," ")
    serve=serve.replace("<li>","")     
    serve=serve.replace("</li>","") 
    cc=db["cosponsors"]
    sponsor=cc.find({"bill_id":{'$regex':"-"+str(meet)},"sponsor":id})
    count_sponsor=0

    for kkk in sponsor:
        count_sponsor=1+count_sponsor
    
    cosponsor=cc.find({"bill_id":{'$regex':"-"+str(meet)},"cosponsors":id})
    count_cosponsor=0
    for kkk in cosponsor:
        count_cosponsor=count_cosponsor+1
    a=[]
    a.append(id)
    a.append(party)
    a.append(x)
    a.append(state)
    a.append(serve) 
    a.append(count_sponsor) 
    a.append(count_cosponsor) 
    print(a)
    return a
    print(id,party,x[0],state[0],serve)
    # html = etree.HTML(driver.page_source)
    # list_url=html.xpath()
    # //*[@id="main"]/ol/li[1]/div[2]/div[2]/span[2]
    
    # return html






def connect():
    myclient = pymongo.MongoClient("210.45.76.110",27017)
    db=myclient["socomp"]
    db.authenticate("socomp","linke-2022")
    return db
def get_group(db,id):
    collection=db["votes"]
    rets=collection.find({"id":id})
    print(rets.count())
    for ret in rets:
        print(ret["group"])   
    # return rets[0]
if __name__ == '__main__':
    db=connect()
    collection=db["members"]
    for i in range(102,117):
        for j in range(0,2):
            print(i,j)
            t=collection.find({"meeting":str(i),"subclub":j},{"members":1})
            for l in t:
                g=l["members"]
                length=len(g)
                for kk in range(length):
                    
                    for ll in range(kk,length):

                        with open(str(i)+str(j)+"e.csv","w",newline="") as csvfile: 
                            writer = csv.writer(csvfile)
                            for item in g:
                                writer.writerow(driver_url(item,i,db))


