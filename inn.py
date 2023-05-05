# 该用于将votes表中的数据按照会议届数和参/众议院 各个议员分开存储，以便于后续的分析
import pymongo
def connect():
    myclient = pymongo.MongoClient("210.45.76.110",27017)
    db=myclient["socomp"]
    db.authenticate("socomp","linke-2022")
    return db

db=connect()
collection=db["members"]
# cc=db["cosponsors"]
vv=db["votes"]
for i in range(102,117):
    for j in range(0,1):
        print(i,j)
        t=collection.find({"meeting":str(i),"subclub":j},{"members":1})#找到第i届 国会 参/众议院的人员名单
        for l in t:
            g=l["members"]
            for kk in range(len(g)):
                name=str(i)+"_"+str(j)+g[kk]
                print(name)
                if name in db.list_collection_names():
                    print("ok")
                    continue
                ccccccc=db[name]
                
                # print(name)
                votes_x=vv.find({"bill_name":{'$regex':"-"+str(i)},"id":g[kk]})
                if votes_x.count()>0:
                    ccccccc.insert_many(votes_x)
