import igraph as ig
# petersen=ig.Graph.Famous('Petersen')
# ig.plot(petersen, layout='kk')
# # ig.save(petersen, 'petersen.png')
# print(petersen)
from sklearn import metrics
import matplotlib.pylab as plt
import csv
import matplotlib.pyplot as plt
# for ttttt in ["1040","1050","1060","1070","1080","1090","1110","1150","1160"]:
for ttttt in ["1100","1120","1130","1140"]:
    print(ttttt)
    csvfile = open(''+ttttt+'.csv', 'r')
    reader = csv.reader(csvfile)
    name=[]
    id=[]
    party=[]
    state=[]
    history=[]
    s=[]
    cos=[]
    for line in reader:
        if len(name)==0:
            name.append(line[2])
            id.append(line[0])
            party.append(line[1])
            state.append(line[3])
            history.append(line[4])
            # s.append(line[5])
            # cos.append(line[6])
        elif line[0] not in name:
            name.append(line[2])
            id.append(line[0])
            party.append(line[1])
            state.append(line[3])
            history.append(line[4])
            # s.append(line[5])
            # cos.append(line[6])
    # g=ig.Graph()
    # g.add_vertices(len(name))
    # g.vs["name"]=name
    # g.vs["id"]=id
    # g.vs["party"]=party
    # g.vs["state"]=state
    # g.vs["history"]=history
    # g.vs["s"]=s
    # g.vs["cos"]=cos
    # color_dict = {"Republican": "red", "Democratic": "blue","Independent":"gray","Unknown":"gray","Independent Democrat":"gray","Libertaria":"gray"}
    # visual_style={}
    # visual_style["vertex_color"]=[color_dict[party_i] for party_i in g.vs["party"]]
    csvfile.close()
    csvfile = open('uv'+ttttt+'.csv', 'r')
    reader = csv.reader(csvfile)
    edge=[]
    correct_s=0
    wrong_s=0
    correct_d=0
    wrong_d=0
    list_t=[]
    list_label=[]
    for line in reader:
        if (line[0],line[1]) not in edge:
            edge.append((line[0],line[1]))
            # if line[2]+line[3]+line[4]!="000":
            if line[7]!="0":
                if line[0] in id and line[1] in id:
                    p_1=party[id.index(line[0])]
                    p_2=party[id.index(line[1])]
                    
                    # g.add_edge(id.index(line[0]),id.index(line[1]))
                    # g.es[-1]["vv"]=line[7]
                    if p_1==p_2 and (p_2=="Democratic" or p_2=="Republican"):
                        list_t.append(float(line[8])/float(line[7]))
                        list_label.append(1)
                        # for i in range(8,26,2):
                        #     if float(line[i])>0:
                        #         correct_s=correct_s+1
                        #         print("1")
                        #     elif float(line[i])<0:
                        #         wrong_s=wrong_s+1   
                    elif (p_2=="Democratic" and p_1=="Republican") or (p_2=="Republican" and p_1=="Democratic"):
                        list_t.append(float(line[8])/float(line[7]))
                        list_label.append(0)
                        # for i in range(8,26,2):
                        #     if float(line[i])<0:
                        #         correct_d=correct_d+1
                        #     elif float(line[i])>0:
                        #         wrong_d=wrong_d+1   
                    # g.es[-1]["sc"]=line[2]
                    # g.es[-1]["cs"]=line[3]
                    # g.es[-1]["cc"]=line[4]
                # g.add_edge(id.index(line[0]),id.index(line[1]))
                # g.es[-1]["vv"]=line[7]
                # g.es[-1]["dist"]=line[8]
                # g.es[-1]["sc"]=line[2]
                # g.es[-1]["cs"]=line[3]
                # g.es[-1]["cc"]=line[4]
    # visual_style["vertex_size"]=5
    # e_color_dist=["green","purple"]
    # # visual_style["edge_width"] = [i+j+k for i,j,k in zip(g.es["sc"],g.es["cs"],g.es["cc"])]
    # # visual_style["edge_width"] = [min(int(i)+int(j)+int(k)/10,7) for i,j,k in zip(g.es["sc"],g.es["cs"],g.es["cc"])]
    # visual_style["edge_color"] = [ e_color_dist[0] if float(i)>0 else e_color_dist[1] for i in g.es["dist"]]
    # visual_style["edge_width"] = [ 1 for i in g.es["dist"]]
    # layout=g.layout("circle")
    # # plt.figure()
    # fig, ax = plt.subplots(1,1)
    # plt.rcParams(figsize=(2000,2000))
    # ig.plot(g, layout=layout ,**visual_style)
    # fig.savefig("social_network_102_0.pdf")

    # ig.plot(g, "social_network_0.pdf", layout=layout ,**visual_style)
    csvfile.close()
    # print(correct_s,wrong_s)
    # print(correct_d,wrong_d)
    # #真实值
    GTlist = list_label
    #模型预测值
    Problist = list_t
    
    # metrics.accuracy_score()
    fpr, tpr, thresholds = metrics.roc_curve(GTlist, Problist, pos_label=1)
    roc_auc = metrics.auc(fpr, tpr)  #auc为Roc曲线下的面积
    print(roc_auc)
    
    plt.figure()
    plt.plot(fpr, tpr, 'b',label='AUC = %0.2f'% roc_auc)
    plt.legend(loc='lower right')
    # plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([-0.1, 1.1])
    plt.ylim([-0.1, 1.1])
    plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
    plt.xlabel('假阳率') #横坐标是fpr
    plt.ylabel('真阳率')  #纵坐标是tpr
    # title = "one-stage approach"
    # title = "归一化投票决策距离的ROC"
    # plt.title(title)
    plt.savefig(ttttt+"_vvvv.png")
    # plt.show()