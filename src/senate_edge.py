
import sys
import pymongo

# edge_options = EdgeOptions()
# # edge_options.use_chromium = True
# # 设置无界面模式，也可以添加其它设置
# edge_options.add_argument('headless')
# # driver = Edge(options=edge_options)
# # r = driver.get('https://www.baidu.com')
# edge_options.binary_location="C:/Users/dell/Desktop/MicrosoftWebDriver.exe"
# chrome_options = Options() # 实例化Option对象
# chrome_options.add_argument('headless') # 把Chrome浏览器设置为静默模式
# # chrome_options.add_argument('disable-gpu') # 禁止加载图片
# driver=webdriver.Edge("C:/Users/dell/Desktop/MicrosoftWebDriver.exe")
# # driver = webdriver.Chrome(options = chrome_options) # 设置引擎为Chrome，在后台默默运行
import csv
# url = 'https://www.congress.gov/search?q=%7B%22source%22%3A%22members%22%2C%22search%22%3A%22O000167%22%7D'


# def driver_url(id,meet,db):
    # url="https://www.congress.gov/search?q=%7B%22source%22%3A%22members%22%2C%22search%22%3A%22"+id+"%22%7D"
    # driver.get(url)
    # # driver.print_page()
    # # driver.get_pinned_scripts()
    # # print(driver.find_element(value="Party"))
    # t=driver.page_source
    # t=t.replace("\n","")
    # D1=re.findall(r"<span>D(.+?)c</span>",t)
    # # print(re.findall(r"<span>R(.+?)n</span>",t))
    # R1=re.findall(r"<span>R(.+?)n</span>",t)

    # # print(re.findall(r"<span>I(.+?)t</span>",t))
    # I1=re.findall(r"<span>In(.+?)t</span>",t)
    # if len(D1)>1:
    #     party="Democratic"
    # elif len(R1)>1:
    #     party="Republican"
    # elif len(I1)>1:
    #     party="In"+I1[0]+"t"
    # else:
    #     party="Unknown"
    # # print(party)
    # x=re.findall(r"<div class=\"member-image\"><img src=\"/img/member/(.+?)></div>",t)
    # x=x[0]
    # x=re.findall(r"alt=\"(.+?)\"",x)
    # x=x[0]
    # # ppp=re.compile(r"<strong>State:</strong><span>(.+?)</span>",re.M)
    # # state=ppp.match(t)
    # t=t.replace(" ","")
    
    # state=re.findall(r"<strong>State:</strong><span>(.+?)</span>",t)
    # if state==[]:
    #     state=["Unknown"]
    # state=state[0]
    # serve=re.findall(r"<ulclass=\"member-served\">(.+?)</ul>",t)
    # if serve==[]:
    #     serve=["Unknown"]
    # serve=serve[0].replace("</li><li>"," ")
    # serve=serve.replace("<li>","")     
    # serve=serve.replace("</li>","") 
    # cc=db["cosponsors"]
    # sponsor=cc.find({"bill_id":{'$regex':"-"+str(meet)},"sponsor":id})
    # count_sponsor=0

    # for kkk in sponsor:
    #     count_sponsor=1+count_sponsor
    
    # cosponsor=cc.find({"bill_id":{'$regex':"-"+str(meet)},"cosponsors":id})
    # count_cosponsor=0
    # for kkk in cosponsor:
    #     count_cosponsor=count_cosponsor+1
    # a=[]
    # a.append(id)
    # a.append(party)
    # a.append(x)
    # a.append(state)
    # a.append(serve) 
    # a.append(count_sponsor) 
    # a.append(count_cosponsor) 
    # print(a)
    # return a
    # print(id,party,x[0],state[0],serve)
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
    ah=['a','b','c','d','e','f','g','h']
    db=connect()
    collection=db["members"]
    vv=db["votes"]

    for i in range(114,101,-1):
    # for i in range(102,117):
        for j in range(1,2):
            print(i,j)
            with open("uv"+str(i)+str(j)+".csv","w",newline="") as csvfile:
                t=collection.find({"meeting":str(i),"subclub":j},{"members":1})#找到第i届 国会 参/众议院的人员名单
                for l in t:
                    g=l["members"]#找到第i届 国会 参/众议院的人员名单
                    length=len(g)#人数
                    for kk in range(length):
                        print(g[kk])
                    # with open("uv"+str(i)+str(j)+".csv","w",newline="") as csvfile: 
                        writer = csv.writer(csvfile)
                        cc=db["cosponsors"]#提案表
                        #g[kk]发起的提案
                        sponsor_x=cc.find({"bill_id":{'$regex':"-"+str(i)},"sponsor":g[kk]})
                        sponsor_xx=[]
                        for kkk in sponsor_x:
                            sponsor_xx.append(kkk["bill_id"])
                        #g[kk]参与的提案
                        cosponsor_x=cc.find({"bill_id":{'$regex':"-"+str(i)},"cosponsors":g[kk]})
                        cosponsor_xx=[]

                        #g[kk]参与的投票
                        for jjj in cosponsor_x:
                            cosponsor_xx.append(jjj["bill_id"])
                        votes_x=vv.find({"bill_name":{'$regex':"-"+str(i)},"id":g[kk]})
                        votes_xx=[]
                        #g[kk]参与的投票 详细信息
                        x_group=None
                        # for lll in votes_x:
                        #     x_group=lll["group"]
                        #     x_district=lll["district"]
                        #     votes_xx.append([lll["bill_name"],lll["bill_type"],lll["vote"]])
                        # if x_group==None:
                        #     continue
                        for ll in range(kk+1,length):
                            #g[ll]发起的提案
                            sponsor_y=cc.find({"bill_id":{'$regex':"-"+str(i)},"sponsor":g[ll]})
                            sponsor_yy=[]
                            for kkk in sponsor_y:
                                sponsor_yy.append(kkk["bill_id"])
                            #g[ll]参与的提案
                            cosponsor_y=cc.find({"bill_id":{'$regex':"-"+str(i)},"cosponsors":g[ll]})
                            cosponsor_yy=[]
                            for jjj in cosponsor_y:
                                cosponsor_yy.append(jjj["bill_id"])
                            #g[ll]参与的投票
                            votes_y=vv.find({"bill_name":{'$regex':"-"+str(i)},"id":g[ll]})
                            votes_yy=[]
                            #详细信息
                            if x_group!=None:
                                y_group=None
                                for lll in votes_y:
                                    y_group=lll["group"]
                                    y_district=lll["district"]
                                    votes_yy.append([lll["bill_name"],lll["bill_type"],lll["vote"]])
                            #统计
                            #投票统计
                            votes_ah=[0,0,0,0,0,0,0,0]
                            dist_ah=[0,0,0,0,0,0,0,0]
                            if x_group!=None:
                                
                                for x in votes_xx:
                                    for y in votes_yy:
                                        if x[0]==y[0]:
                                            ind=[h for h,alpha in enumerate(ah) if x[1]==alpha]
                                            ind=ind[0]
                                            votes_ah[ind]=votes_ah[ind]+1
                                            if x[2]==y[2]: 
                                                dist_ah[ind]=dist_ah[ind]+1
                                            elif x[2]=='NV' or y[2]=='NV':
                                                dist_ah[ind]=dist_ah[ind]+0.5
                                            else:
                                                dist_ah[ind]=dist_ah[ind]-1

                            u_s_v_c=len([x for x in sponsor_xx if x in cosponsor_yy])
                            u_c_v_s=len([x for x in sponsor_yy if x in cosponsor_xx])
                            u_c_v_c=len([x for x in cosponsor_xx if x in cosponsor_yy])
                            
                            # if x_group!=None and y_group!=None:
                            writer.writerow([g[kk],g[ll],u_s_v_c,u_c_v_s,u_c_v_c,len(votes_xx),len(votes_yy)
                                                ,sum(votes_ah),sum(dist_ah),
                                                votes_ah[0],dist_ah[0],
                                                votes_ah[1],dist_ah[1],
                                                votes_ah[2],dist_ah[2],
                                                votes_ah[3],dist_ah[3],
                                                votes_ah[4],dist_ah[4],
                                                votes_ah[5],dist_ah[5],
                                                votes_ah[6],dist_ah[6],
                                                votes_ah[7],dist_ah[7],
                                                ])
                #             print([g[kk],g[ll],u_s_v_c,u_c_v_s,u_c_v_c,len(votes_xx),len(votes_yy)
                #                                 ,sum(votes_ah),sum(dist_ah),
                #                                 votes_ah[0],dist_ah[0],
                #                                 votes_ah[1],dist_ah[1],
                #                                 votes_ah[2],dist_ah[2],
                #                                 votes_ah[3],dist_ah[3],
                #                                 votes_ah[4],dist_ah[4],
                #                                 votes_ah[5],dist_ah[5],
                #                                 votes_ah[6],dist_ah[6],
                #                                 votes_ah[7],dist_ah[7],
                #                                 ])
                #             break
                #         break
                #     break
                # break
                            # print([g[kk],g[ll],x_group,x_district,y_group,y_district,len(votes_xx),len(votes_yy)
                            #                  ,u_s_v_c,u_c_v_s,u_c_v_c,sum(votes_ah),sum(dist_ah),
                            #                  votes_ah[0],dist_ah[0],
                            #                  votes_ah[1],dist_ah[1],
                            #                  votes_ah[2],dist_ah[2],
                            #                  votes_ah[3],dist_ah[3],
                            #                  votes_ah[4],dist_ah[4],
                            #                  votes_ah[5],dist_ah[5],
                            #                  votes_ah[6],dist_ah[6],
                            #                  votes_ah[7],dist_ah[7],
                            #                  ])

