import igraph as ig
import networkx as nx
import csv
import matplotlib.pyplot as plt
# plt.axis('off')
B=nx.Graph()
csvfile = open('1020 copy.csv', 'r')
reader = csv.reader(csvfile)
name=[]
id=[]
party=[]
state=[]
history=[]
s=[]
cos=[]
nodet=[]
size=[]
node_color=[]
#读取参众议员的信息
#众议院
Z_ID=[]
D_ID=[]
R_ID=[]
for line in reader:
    if line[0] not in id:
        nodet.append(0)
        size.append(3)
        Z_ID.append(line[0])
        name.append(line[2])
        id.append(line[0])
        party.append(line[1])
        state.append(line[3])
        history.append(line[4])
        s.append(line[5])
        cos.append(line[6])
        node_color.append('blue' if line[1]=="Democratic" else "red")
        if line[1]=="Democratic":
            D_ID.append(line[0])
        else :
            R_ID.append(line[0])
        
csvfile.close()
B.add_nodes_from(Z_ID,bipartite=0)
#参议院
C_ID=[]

csvfile = open('1021 copy.csv', 'r')
reader = csv.reader(csvfile)
for line in reader:
    if line[0] not in id:
        nodet.append(1)
        size.append(5)
        C_ID.append(line[0])
        # if line[]/
        name.append(line[2])
        id.append(line[0])
        party.append(line[1])
        state.append(line[3])
        history.append(line[4])
        s.append(line[5])
        cos.append(line[6])
        node_color.append('blue' if line[1]=="Democratic" else "red")
        if line[1]=="Democratic":
            D_ID.append(line[0])
        else :
            R_ID.append(line[0])
csvfile.close()#获取参众议员的列表
B.add_nodes_from(C_ID,bipartite=1)
#读取参众议员之间的关系
csvfile = open('102_start/uv102.csv', 'r')
reader = csv.reader(csvfile)
edge=[]
dist=[]
eeeee=[]
count_E=[]
for line in reader:
    if line[0] in Z_ID and line[1] in C_ID:
        xxxxxxxx=(id.index(line[0]),id.index(line[1]))
        if xxxxxxxx not in edge:
            edge.append(xxxxxxxx)
            eeeee.append((line[0],line[1]))
            dist.append(float(line[3]))
            count_E.append(1)
        else:
            if line[0] in id and line[1] in id:
                e_id=edge.index(xxxxxxxx)
                count_E[e_id]=count_E[e_id]+1
                dist[e_id]=dist[e_id]+float(line[3])

edge_color=[]
e_color_dist=["green","purple"]

for i in range(len(dist)):
    dist[i]=dist[i]/count_E[i]
    # dist[i]=20*(dist[i]-mi)/(ma-mi)
# edge_color = [ e_color_dist[0] if float(i)>0 else e_color_dist[1] for i in dist]
ma=max(dist)
mi=min(dist)
edge_color=dist
B.add_edges_from(eeeee)

# remove = [node for node,degree in dict(B.degree()).items() if degree <1]
# B.remove_nodes_from(remove)

# m, n = 5, 10
# K = nx.complete_bipartite_graph(m, n)
m=len(Z_ID)
n=len(C_ID)
pos = {}
pos.update((Z_ID[i], (5*(i - m/2), 1)) for i in range(m))
pos.update((C_ID[i-m], (20*(i - m - n/2), 0)) for i in range(m, m + n))

# fig, ax = plt.subplots()
# fig.set_size_inches(15, 4)
# nx.draw(K, with_labels=True, pos=pos, node_size=300, width=0.4)
# plt.show()
ax1=plt.gca()
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(False)


plt.figure(figsize=(5,4))
nx.draw_networkx(
    B,
    # pos = nx.drawing.layout.bipartite_layout(B, Z_ID,align='horizontal',aspect_ratio=10),
    pos = pos,node_size=size
    ,with_labels=False,node_color=node_color,edge_color=edge_color,edge_cmap=plt.cm.Blues,linewidths=0,ax=ax1,vmin=mi,vmax=ma)

plt.show()
# g=ig.Graph.Bipartite(types=nodet,edges=edge,directed=False)
# g.vs["name"]=name
# g.vs["id"]=id
# g.vs["party"]=party
# g.vs["state"]=state
# g.vs["history"]=history
# g.vs["s"]=s
# g.vs["cos"]=cos
# g.es["dist"]=dist
# csvfile = open('102_start/uv102.csv', 'r')
# reader = csv.reader(csvfile)

# # for line in reader:
# #     if (line[0],line[1]) not in edge:
# #         edge.append((line[0],line[1]))
# #         g.add_edge(id.index(line[0]),id.index(line[1]))
# #         g.es[-1]["dist"]=line[3]
# color_dict = {"Republican": "red", "Democratic": "blue","Independent":"gray","Unknown":"gray","Independent Democrat":"gray","Libertaria":"gray"}
# visual_style={}
# visual_style["vertex_color"]=[color_dict[party_i] for party_i in g.vs["party"]]
# csvfile.close()

# visual_style["vertex_size"]=3
# e_color_dist=["green","purple"]
# # visual_style["edge_width"] = [i+j+k for i,j,k in zip(g.es["sc"],g.es["cs"],g.es["cc"])]
# # visual_style["edge_width"] = [min(int(i)+int(j)+int(k)/10,7) for i,j,k in zip(g.es["sc"],g.es["cs"],g.es["cc"])]
# visual_style["edge_color"] = [ e_color_dist[0] if float(i)>0 else e_color_dist[1] for i in g.es["dist"]]
# visual_style["edge_width"] = [ 1 for i in g.es["dist"]]

# # layout=g.layout("kk")
# # plt.figure()
# # fig, ax = plt.subplots(1,1)
# # plt.rcParams(figsize=(2000,2000))
# # ig.plot(g, layout=layout ,**visual_style)
# # fig.savefig("social_network_102_0.pdf")
# de=g.degree()
# for i in range(len(de)-1,-1,-1):
#     if de[i]==0:
#         g.delete_vertices(i)
# g.layout_bipartite(types="type", hgap=1, vgap=1, maxiter=100)

# ig.plot(g, "social_network_bi.pdf", **visual_style)
# csvfile.close()