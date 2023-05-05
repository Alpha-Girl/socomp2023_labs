import igraph as ig
# petersen=ig.Graph.Famous('Petersen')
# ig.plot(petersen, layout='kk')
# # ig.save(petersen, 'petersen.png')
# print(petersen)
import csv
csvfile = open('1021 copy.csv', 'r')
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
        s.append(line[5])
        cos.append(line[6])
    elif line[0] not in name:
        name.append(line[2])
        id.append(line[0])
        party.append(line[1])
        state.append(line[3])
        history.append(line[4])
        s.append(line[5])
        cos.append(line[6])
g=ig.Graph()
g.add_vertices(len(name))
g.vs["name"]=name
g.vs["id"]=id
g.vs["party"]=party
g.vs["state"]=state
g.vs["history"]=history
g.vs["s"]=s
g.vs["cos"]=cos
color_dict = {"Republican": "red", "Democratic": "blue","Independent":"gray","Unknown":"gray","Independent Democrat":"gray","Libertaria":"gray"}
visual_style={}
visual_style["vertex_color"]=[color_dict[party_i] for party_i in g.vs["party"]]
csvfile.close()
csvfile = open('uv1021.csv', 'r')
reader = csv.reader(csvfile)
edge=[]
for line in reader:
    if (line[0],line[1]) not in edge:
        edge.append((line[0],line[1]))
        if line[2]+line[3]+line[4]!="000":
            g.add_edge(id.index(line[0]),id.index(line[1]))
            g.es[-1]["sc"]=line[2]
            g.es[-1]["cs"]=line[3]
            g.es[-1]["cc"]=line[4]
visual_style["vertex_size"]=10
# visual_style["edge_width"] = [i+j+k for i,j,k in zip(g.es["sc"],g.es["cs"],g.es["cc"])]
visual_style["edge_width"] = [min(int(i)+int(j)+int(k)/10,7) for i,j,k in zip(g.es["sc"],g.es["cs"],g.es["cc"])]
layout=g.layout("graphopt")
ig.plot(g, "social_network.pdf", layout=layout ,**visual_style)