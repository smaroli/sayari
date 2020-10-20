import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv('./sayari/spiders/northdakotaexport.csv', sep = ',',index_col=0)

#Build the graph with nodes for title (red), owner(yellow), registered agent(blue) and commercial registered agent(green)
G=nx.Graph()   
G.add_nodes_from(df.TITLE,color = 'red')
G.add_nodes_from(df.OWNER, color = 'yellow')
G.add_nodes_from(df.RA, color = 'blue')
G.add_nodes_from(df.CRA, color = 'green')

#creating edges for title and owner
subset = df[['TITLE','OWNER']]
tuples = [tuple(x) for x in subset.values] 
for each in tuples:
	if pd.isna(each[1]):
		pass
	else:
		G.add_edge(each[0],each[1])

#creating edges for title and registered agent
subset1 = df[['TITLE','RA']]
tuples1 = [tuple(x) for x in subset1.values] 
for each in tuples1:
	if pd.isna(each[1]):
		pass
	else:
		G.add_edge(each[0],each[1])

#creating edges for title and commercial registered agent		
subset2 = df[['TITLE','CRA']]
tuples2 = [tuple(x) for x in subset2.values] 
for each in tuples2:
	if pd.isna(each[1]):
		pass
	else:
		G.add_edge(each[0],each[1])

#removing empty nodes (without edges) if any
#for n in G.nodes():
    #if n == '':
        #G.remove_node(n)

#add colors to the network graph for each type of node
color_map = []
for n in G.nodes():
    color_map.append(G.node[n]['color'])

#plot graph and save	
plt.figure(figsize=(100,100))
nx.draw_networkx(G, node_color = color_map, with_labels = False, node_size = 50)
plt.savefig('northdakotaplot.png')
plt.show()
