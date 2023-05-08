import csv
id_list=["B001236"]
# for i in range(102,117):
#     for j in range(0,2):
#         csvfile = open(str(i)+str(j)+'.csv', 'r')
#         reader = csv.reader(csvfile)
#         for line in reader:
#             if line[0] not in id_list:
#                 id_list.append(line[0])
# csvfile.close()
for id in id_list:
    senate=[]
    house=[]
    senate_s=[]
    senate_c=[]
    house_s=[]
    house_c=[]
    # id="J000177"
    for i in range(102,117):
        for j in range(0,2):
            csvfile = open(str(i)+str(j)+'.csv', 'r')
            reader = csv.reader(csvfile)
            for line in reader:
                if line[0]==id:
                    if j==1:
                        senate.append(i)
                        senate_s.append(int(line[5]))
                        senate_c.append(int(line[6]))
                    else:
                        house.append(i)
                        house_s.append(int(line[5]))
                        house_c.append(int(line[6]))
            csvfile.close()
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12,8))
    plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
    # plt.rcParams['font.size']=["10"]
    # plt.xlim([101,117])
    # plt.ylim([-1,max(max(senate_s),max(senate_c),max(house_s),max(house_c))+5])
    if len(senate)>0 or len(house)>0:
        if len(senate)>0:
            plt.plot( senate,senate_s,'r*--',label="在参议院发起")
            plt.plot( senate,senate_c,'bs--',label="在参议院联合发起")
        if len(house)>0:
            plt.plot( house,house_c,'go--',label="在众议院发起")
            plt.plot( house,house_s,'yx--',label="在众议院联合发起")
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.legend(fontsize=20)
        plt.xlabel("届别",fontsize=20)
        plt.ylabel("提案数",fontsize=20)
        plt.savefig("img/"+id+".png")