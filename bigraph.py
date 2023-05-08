
import sys
import pymongo

import csv

def connect():
    myclient = pymongo.MongoClient("210.45.76.110",27017)
    db=myclient["socomp"]
    db.authenticate("socomp","linke-2022")
    return db
def dist(t):
    if t=="Y":
        return 1
    elif t=="N":
        return -1
    else:
        return 0.5
if __name__ == '__main__':
    ah=['a','b','c','d','e','f','g','h']
    db=connect()
    collection=db["members"]
    # for i in range(116,101,-1):
    for i in range(102,117):
        for j in range(0,1):
            print(i,j)
            with open("102_start/uv"+str(i)+".csv","w",newline="") as csvfile:
                writer = csv.writer(csvfile)
                cc=db["cosponsors"]
                t=collection.find({"meeting":str(i),"subclub":0},{"members":1})#找到第i届 国会 众议院的人员名单
                for l in t:
                    g=l["members"]#找到第i届 国会 众议院的人员名单
                    new_g=list(set(g))
                    new_g.sort(key=g.index)
                    g=new_g
                    length=len(g)#人数
                    for kk in range(length):
                        print(g[kk])
                        vv=db[str(i)+"_0"+g[kk]]
                        votes_x=vv.find()
                        votes_xx=[]
                        for lll in votes_x:
                            x_group=lll["group"]
                            x_district=lll["district"]
                            votes_xx.append([lll["bill_name"],lll["bill_type"],lll["vote"],lll["date"]])
                        for bb in votes_xx:
                            tmp_x=cc.find({"bill_id":bb[0]})
                            for bbb in tmp_x:
                                writer.writerow([g[kk],bbb["sponsor"],bb[1],dist(bb[2])])
                                for cos in bbb["cosponsors"]:
                                    writer.writerow([g[kk],cos,bb[1],dist(bb[2])])
                    # # with open("uv"+str(i)+str(j)+".csv","w",newline="") as csvfile: 
                        
                    #     #提案表
                    #     #g[kk]发起的提案
                    #     sponsor_x=cc.find({"bill_id":{'$regex':"-"+str(i)},"sponsor":g[kk]})
                    #     sponsor_xx=[]
                    #     for kkk in sponsor_x:
                    #         sponsor_xx.append(kkk["bill_id"])
                    #     #g[kk]参与的提案
                    #     cosponsor_x=cc.find({"bill_id":{'$regex':"-"+str(i)},"cosponsors":g[kk]})
                    #     cosponsor_xx=[]

                    #     #g[kk]参与的投票
                    #     for jjj in cosponsor_x:
                    #         cosponsor_xx.append(jjj["bill_id"])
                    #     vv=db[str(i)+"_"+str(j)+g[kk]]
                    #     votes_xx=[]
                    #     #g[kk]参与的投票 详细信息
                    #     x_group=None
                        
                    #     # if x_group==None:
                    #     #     continue
                    #     for ll in range(kk+1,length):
                    #         #g[ll]发起的提案
                    #         sponsor_y=cc.find({"bill_id":{'$regex':"-"+str(i)},"sponsor":g[ll]})
                    #         sponsor_yy=[]
                    #         for kkk in sponsor_y:
                    #             sponsor_yy.append(kkk["bill_id"])
                    #         #g[ll]参与的提案
                    #         cosponsor_y=cc.find({"bill_id":{'$regex':"-"+str(i)},"cosponsors":g[ll]})
                    #         cosponsor_yy=[]
                    #         for jjj in cosponsor_y:
                    #             cosponsor_yy.append(jjj["bill_id"])
                    #         #g[ll]参与的投票
                    #         vv=db[str(i)+"_"+str(j)+g[ll]]
                    #         votes_y=vv.find()
                    #         votes_yy=[]
                    #         #详细信息
                    #         if x_group!=None:
                    #             y_group=None
                    #             for lll in votes_y:
                    #                 y_group=lll["group"]
                    #                 y_district=lll["district"]
                    #                 votes_yy.append([lll["bill_name"],lll["bill_type"],lll["vote"],lll["date"]])
                    #         #统计
                    #         #投票统计
                    #         votes_ah=[0,0,0,0,0,0,0,0]
                    #         dist_ah=[0,0,0,0,0,0,0,0]
                    #         if x_group!=None:
                                
                    #             for x in votes_xx:
                    #                 for y in votes_yy:
                    #                     if x[0]==y[0] and x[3]==y[3]:
                    #                         ind=[h for h,alpha in enumerate(ah) if x[1]==alpha]
                    #                         ind=ind[0]
                    #                         votes_ah[ind]=votes_ah[ind]+1
                    #                         if x[2]==y[2]: 
                    #                             dist_ah[ind]=dist_ah[ind]+1
                    #                         elif x[2]=='NV' or y[2]=='NV':
                    #                             dist_ah[ind]=dist_ah[ind]+0.5
                    #                         else:
                    #                             dist_ah[ind]=dist_ah[ind]-1

                    #         u_s_v_c=len([x for x in sponsor_xx if x in cosponsor_yy])
                    #         u_c_v_s=len([x for x in sponsor_yy if x in cosponsor_xx])
                    #         u_c_v_c=len([x for x in cosponsor_xx if x in cosponsor_yy])
                            
                    #         # if x_group!=None and y_group!=None:
                    #         writer.writerow([g[kk],g[ll],u_s_v_c,u_c_v_s,u_c_v_c,len(votes_xx),len(votes_yy)
                    #                             ,sum(votes_ah),sum(dist_ah),
                    #                             votes_ah[0],dist_ah[0],
                    #                             votes_ah[1],dist_ah[1],
                    #                             votes_ah[2],dist_ah[2],
                    #                             votes_ah[3],dist_ah[3],
                    #                             votes_ah[4],dist_ah[4],
                    #                             votes_ah[5],dist_ah[5],
                    #                             votes_ah[6],dist_ah[6],
                    #                             votes_ah[7],dist_ah[7],
                    #                             ])
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

