import pymongo
from urllib.request import Request,urlopen
from urllib.parse import quote
import string
import pyhttpx

headers = {
    "Accept": "*/*",
    "Cookie": "DSID=AJ0cbrl4L0za5iv_hE9PEVCC8-hPicRk3GmX6e6W3xUmfG5MTFd1zjBv4AyM-_k1TRRKhOEC-EyXpUk-h85OLv7NDL6ppa3XguCZWv6j2ivOT-DhvzUx94E4DhUTMbR8Ke_Hajrof3o87rFAAcKxEroAA6_im2Q-u5Lnf0NyGhlAR0c8ZTvT2BhSK715sYO2nL3eAgP84lxorXlDwRCfgxEzPYqdXDarntRtysN1qqDIZRrHRF6N3ZI0wM7B4cCutvCnJ6op8akot2fy_6zalj1oqUmZ-7gFZo3ADt1nSDLeSXqXW_RSqwA; id=22e4ec8ef6d9008f||t=1676622386|et=730|cs=002213fd484c0f283260f04d29",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
}
session = pyhttpx.HttpSession()
res = session.get(url='https://www.congress.gov/search?q=%7B%22source%22%3A%22members%22%2C%22search%22%3A%22O000167%22%7D',headers=headers)
print(res.content.decode('utf-8'))
# print(res.json.encode('utf-8'))
res.encoding = 'utf-8'
print(res.text)
# url = 'https://www.congress.gov/search?q=%7B%22source%22%3A%22members%22%2C%22search%22%3A%22O000167%22%7D'
# # headers = {'User-Agent':'Edg/112.0.1722.68'}
# # url = Request(url,headers=headers)
# # html = urlopen(url).read().decode('utf-8')
# from urllib.request import urlopen,Request
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}
# url = Request(url, headers=headers)
# r=urlopen(url,timeout=10)
# def connect():
#     myclient = pymongo.MongoClient("210.45.76.110",27017)
#     db=myclient["socomp"]
#     db.authenticate("socomp","linke-2022")
#     return db
# def get_group(db,id):
#     collection=db["votes"]
#     rets=collection.find({"id":id})
#     print(rets.count())
#     for ret in rets:
#         print(ret["group"])   
#     # return rets[0]
                                   
# db=connect()
# # get_group(db,"B000444")

# get_group(db,"O000167")