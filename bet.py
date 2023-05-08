import random
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, Normalize
import igraph as ig
import csv
def plot_betweenness(g, vertex_betweenness, edge_betweenness, ax, cax1, cax2):
    '''Plot vertex/edge betweenness, with colorbars

    Args:
        g: the graph to plot.
        ax: the Axes for the graph
        cax1: the Axes for the vertex betweenness colorbar
        cax2: the Axes for the edge betweenness colorbar
    '''

    # Rescale betweenness to be between 0.0 and 1.0
    scaled_vertex_betweenness = ig.rescale(vertex_betweenness, clamp=True)
    scaled_edge_betweenness = ig.rescale(edge_betweenness, clamp=True)
    print(f"vertices: {min(vertex_betweenness)} - {max(vertex_betweenness)}")
    print(f"edges: {min(edge_betweenness)} - {max(edge_betweenness)}")

    # Define mappings betweenness -> color
    cmap1 = LinearSegmentedColormap.from_list("vertex_cmap", ["pink", "indigo"])
    cmap2 = LinearSegmentedColormap.from_list("edge_cmap", ["lightblue", "midnightblue"])

    # Plot graph
    g.vs["color"] = [cmap1(betweenness) for betweenness in scaled_vertex_betweenness]
    g.vs["size"]  = ig.rescale(vertex_betweenness, (0.1, 0.5))
    g.es["color"] = [cmap2(betweenness) for betweenness in scaled_edge_betweenness]
    g.es["width"] = ig.rescale(edge_betweenness, (0.5, 1.0))
    ig.plot(
        g,
        target=ax,
        layout="fruchterman_reingold",
        # layout="circle",
        vertex_frame_width=0.2,
    )

    # Color bars
    norm1 = ScalarMappable(norm=Normalize(0, max(vertex_betweenness)), cmap=cmap1)
    norm2 = ScalarMappable(norm=Normalize(0, max(edge_betweenness)), cmap=cmap2)
    plt.colorbar(norm1, cax=cax1, orientation="horizontal", label='Vertex Betweenness')
    plt.colorbar(norm2, cax=cax2, orientation="horizontal", label='Edge Betweenness')
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
# layout=g.layout("graphopt")
# ig.plot(g, "social_network.pdf", layout=layout ,**visual_style)
vertex_betweenness1 = g.betweenness()
edge_betweenness1 = g.edge_betweenness()
fig, axs = plt.subplots(
    3, 1,
    figsize=(6, 9),
    gridspec_kw=dict(height_ratios=(20, 1, 1)),
)
plot_betweenness(g, vertex_betweenness1, edge_betweenness1, *axs[:])
# plot_betweenness(g2, vertex_betweenness2, edge_betweenness2, *axs[:, 1])
fig.tight_layout(h_pad=1)
# plt.show()
plt.savefig("1021bet.pdf")