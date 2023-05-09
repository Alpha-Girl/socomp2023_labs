import csv
#提取众议员 及其是否在任期后加入众议院
import pymongo
def connect():
    myclient = pymongo.MongoClient("210.45.76.110",27017)
    db=myclient["socomp"]
    db.authenticate("socomp","linke-2022")
    return db
# id_list=["B001236"]
id_list=[]
#查找议员列表
def get_senate(t):
    t=t.replace("Present","2023")
    t=t.split()
    flag_house=0
    flag_senate=0
    in_house=[]
    in_senate=[]
    for i in t:
        if i.find("House")>-1:
            flag_house=1
            ii=i.replace("House:","")
            x=ii.split(",")
            for j in x:
                if len(j)>5:
                    for k in range(int(j[0:4]),int(j[5:9]),2):
                        in_house.append(int((k-1)/2-995+102))
                        # in_house[(k-1)/2-995]=1/
                else:
                    in_house.append(int((int(j[0:4])-1)/2-995+102))
            if in_house[-1]<102:
                flag_house=0
        if i.find("Senate")>-1:
            flag_senate=1
            ii=i.replace("Senate:","")
            x=ii.split(",")
            # print(x)
            for j in x:
                if len(j)>5:
                    if j[0:4]=="2023":
                        in_senate.append(118)
                    else:
                        for k in range(int(j[0:4]),int(j[5:9]),2):
                            in_senate.append(int((k-1)/2-995+102))
                
                else:
                    in_senate.append(int((int(j[0:4])-1)/2-995+102))
                    # in_house[(k-1)/2-995]=1/
            
    return flag_house,flag_senate,in_house
node=[]
node_id=[]
node_s=[]
node_ll=[]
node_party=[]
with open("htos.csv","w",newline="") as csvfile1: 
    writer = csv.writer(csvfile1)

# csvfile1=open('')
    for i in range(102,117):
        for j in range(0,2):
            csvfile = open(str(i)+str(j)+'.csv', 'r')
            reader = csv.reader(csvfile)
            for line in reader:
                if line[0] not in id_list:
                    id_list.append(line[0])
                    h,s,ll=get_senate(line[4])
                    if h==1:
                        if 117 not in ll:
                            writer.writerow([line[0],s]+ll)
                            node.append([line[0],s,ll])
                            node_id.append(line[0])
                            node_s.append(s)
                            node_ll.append(ll)
                            node_party.append(line[1])
                    #     print([line[0],s]+ll)
                    # print(line[0],get_senate(line[4]))

    csvfile.close()
# csvfile1.close()
# print(node)
db=connect()
with open("htos_node_x.csv","w",newline="") as csvfile1: 
    writer = csv.writer(csvfile1)
    for o in range(len(node_id)):
        print(o)
        id=node_id[o]

        senate=[]
        house=[]
        senate_s=[]
        senate_c=[]
        house_s=[]
        house_c=[]
        # id="J000177"
        tmp=0
        for i in range(102,117):
            for j in range(0,1):
                csvfile = open(str(i)+str(j)+'.csv', 'r')
                reader = csv.reader(csvfile)
                for line in reader:
                    if line[0]==id:
                        # if j==1:
                        #     senate.append(i)
                        #     senate_s.append(int(line[5]))
                        #     senate_c.append(int(line[6]))
                        # else:
                        house.append(i)
                        house_s.append(int(line[5]))
                        house_c.append(int(line[6]))
                csvfile.close()
                # csvfile = open("uv"+str(i)+'0.csv', 'r')
                # reader = csv.reader(csvfile)
                
                # for line in reader:
                #     if line[0]==id and int(line[7]) >0:

                #         tmp=tmp+float(line[8])/float(line[7])
                # csvfile.close()
        # writer.writerow([id,node_s[o],sum(house_s)/len(house_s),sum(house_c)/len(house_c),tmp/len(house_s)])
        collection=db["cosponsors"]
        res=collection.find({"sponsor":id})
        actions_dates=0
        a,b,c,d,e,f,g,h=0,0,0,0 ,0,0,0,0
        for ret in res:
            actions_dates=actions_dates+len(ret["actions_dates"])
            if ret["bill_type"]=="a":
                a=a+1
            elif ret["bill_type"]=="b":
                b=b+1
            elif ret["bill_type"]=="c":
                c=c+1
            elif ret["bill_type"]=="d":
                d=d+1
            elif ret["bill_type"]=="e":
                e=e+1
            elif ret["bill_type"]=="f":
                f=f+1
            elif ret["bill_type"]=="g":
                g=g+1
            elif ret["bill_type"]=="h":
                h=h+1
        res=collection.find({"cosponsors":id})
        actions_dates_c=0
        a_c,b_c,c_c,d_c,e_c,f_c,g_c,h_c=0,0,0,0 ,0,0,0,0
        for ret in res:
            actions_dates_c=actions_dates_c+len(ret["actions_dates"])
            if ret["bill_type"]=="a":
                a_c=a_c+1
            elif ret["bill_type"]=="b":
                b_c=b_c+1
            elif ret["bill_type"]=="c":
                c_c=c_c+1
            elif ret["bill_type"]=="d":
                d_c=d_c+1
            elif ret["bill_type"]=="e":
                e_c=e_c+1
            elif ret["bill_type"]=="f":
                f_c=f_c+1
            elif ret["bill_type"]=="g":
                g_c=g_c+1
            elif ret["bill_type"]=="h":
                h_c=h_c+1
        writer.writerow([id,node_s[o],sum(house_s)/len(house_s),sum(house_c)/len(house_c),
                         house_s[-1],
                         house_s[-1]-house_s[-2] if len(house_s)>1 else 0,
                         house_s[-2]-house_s[-3] if len(house_s)>2 else 0,
                         house_c[-1],
                         house_c[-1]-house_c[-2] if len(house_c)>1 else 0,
                         house_c[-2]-house_c[-3] if len(house_c)>2 else 0,
                         a,b,c,d,e,f,g,h,actions_dates/(a+b+c+d+e+f+g+h+1),
                         a_c,b_c,c_c,d_c,e_c,f_c,g_c,h_c,actions_dates/(a_c+b_c+c_c+d_c+e_c+f_c+g_c+h_c+1)
                         ])
        # print()
    # import matplotlib.pyplot as plt
    # plt.figure(figsize=(12,8))
    # plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
    # # plt.rcParams['font.size']=["10"]
    # # plt.xlim([101,117])
    # # plt.ylim([-1,max(max(senate_s),max(senate_c),max(house_s),max(house_c))+5])
    # if len(senate)>0 or len(house)>0:
    #     if len(senate)>0:
    #         plt.plot( senate,senate_s,'r*--',label="在参议院发起")
    #         plt.plot( senate,senate_c,'bs--',label="在参议院联合发起")
    #     if len(house)>0:
    #         plt.plot( house,house_c,'go--',label="在众议院发起")
    #         plt.plot( house,house_s,'yx--',label="在众议院联合发起")
    #     plt.xticks(fontsize=20)
    #     plt.yticks(fontsize=20)
    #     plt.legend(fontsize=20)
    #     plt.xlabel("届别",fontsize=20)
    #     plt.ylabel("提案数",fontsize=20)
    #     plt.savefig("img/"+id+".png")