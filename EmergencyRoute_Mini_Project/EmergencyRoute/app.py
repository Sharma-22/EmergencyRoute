import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import heapq

st.set_page_config(page_title='EmergencyRoute', page_icon='🚑', layout='wide')
st.markdown('''<style>.block-container{padding-top:1.5rem}.hero{padding:1.2rem 1.4rem;border-radius:14px;background:linear-gradient(120deg,#10243a,#174d67);color:white}.hero h1{color:white;margin:0}.hero p{color:#e4f2fa;margin:.35rem 0 0}</style><div class="hero"><h1>🚑 EmergencyRoute</h1><p>Emergency Vehicle Route Optimizer · DAA Mini Project</p></div>''', unsafe_allow_html=True)
st.warning('Educational prototype only: road distances and traffic are sample/simulated data, not live GPS or real-time traffic. Do not use for actual emergency dispatch.')

# Illustrative sample road network: (location A, location B, distance in km, base travel time in minutes)
ROADS = [
 ('Ambulance Base','City Square',3.0,4),('Ambulance Base','Green Park',4.2,5),
 ('City Square','Central Market',2.4,3),('City Square','Civil Hospital Junction',3.5,4),
 ('Green Park','University Gate',2.2,2),('University Gate','Civil Hospital Junction',2.8,3),
 ('University Gate','Lake Road',3.1,3),('Central Market','Civil Hospital Junction',1.7,2),
 ('Central Market','Bus Stand',2.5,3),('Bus Stand','Civil Hospital Junction',2.2,3),
 ('Bus Stand','District Hospital',4.0,4),('Civil Hospital Junction','District Hospital',2.6,3),
 ('Lake Road','District Hospital',5.0,5),('Lake Road','Medical College',3.4,3),
 ('Medical College','District Hospital',2.0,2),('Central Market','Medical College',4.1,4)]
STARTS=['Ambulance Base','City Square','Green Park','University Gate','Central Market','Bus Stand']
HOSPITALS=['District Hospital','Medical College']


def build_graph(level):
    G=nx.Graph(); multiplier={'Low':1.0,'Moderate':1.35,'Heavy':1.8}[level]
    congestion={frozenset(('City Square','Central Market')),frozenset(('Central Market','Bus Stand')),frozenset(('Central Market','Civil Hospital Junction'))}
    for u,v,km,base in ROADS:
        m=multiplier
        if level=='Heavy' and frozenset((u,v)) in congestion: m*=2
        G.add_edge(u,v,distance=km,minutes=max(1,round(base*m)))
    return G

def dijkstra(G, source, target, weight):
    dist={n:float('inf') for n in G}; prev={}; dist[source]=0; queue=[(0,source)]; visited=set()
    while queue:
        cost,node=heapq.heappop(queue)
        if node in visited: continue
        visited.add(node)
        if node==target: break
        for nxt,data in G[node].items():
            new=cost+data[weight]
            if new<dist[nxt]: dist[nxt]=new; prev[nxt]=node; heapq.heappush(queue,(new,nxt))
    if dist[target]==float('inf'): return None,dist[target]
    path=[]; cur=target
    while cur!=source: path.append(cur); cur=prev[cur]
    path.append(source); path.reverse(); return path,dist[target]

def stats(G,path):
    return (sum(G[u][v]['distance'] for u,v in zip(path,path[1:])),sum(G[u][v]['minutes'] for u,v in zip(path,path[1:]))) if path else (0,0)

def draw_graph(G,path,start,target):
    pos={'Ambulance Base':(0,2.1),'Green Park':(1.2,3.4),'University Gate':(2.7,3.5),'Lake Road':(4.1,3.5),'Medical College':(5.3,2.5),'City Square':(1.2,1.6),'Central Market':(2.7,1.7),'Bus Stand':(4,1.2),'Civil Hospital Junction':(3.8,2.5),'District Hospital':(5.4,1.1)}
    fig,ax=plt.subplots(figsize=(10,5)); nx.draw_networkx_edges(G,pos,ax=ax,edge_color='#9aa8b5',width=1.6)
    nx.draw_networkx_nodes(G,pos,ax=ax,node_color='#dceaf5',edgecolors='#2c5f7d',node_size=1550)
    if path:
        nx.draw_networkx_edges(G,pos,edgelist=list(zip(path,path[1:])),ax=ax,edge_color='#df3e48',width=4)
        nx.draw_networkx_nodes(G,pos,nodelist=path,ax=ax,node_color='#ffd8d8',edgecolors='#df3e48',node_size=1550)
    nx.draw_networkx_nodes(G,pos,nodelist=[start],ax=ax,node_color='#b6edc8',edgecolors='#218447',node_size=1700)
    nx.draw_networkx_nodes(G,pos,nodelist=[target],ax=ax,node_color='#ffe7a6',edgecolors='#b58100',node_size=1700)
    nx.draw_networkx_labels(G,pos,ax=ax,font_size=8,font_weight='bold')
    labels={(u,v):f"{d['distance']} km" for u,v,d in G.edges(data=True)}; nx.draw_networkx_edge_labels(G,pos,edge_labels=labels,ax=ax,font_size=7,rotate=False)
    ax.axis('off'); fig.tight_layout(); return fig

with st.sidebar:
    st.header('Route Settings')
    start=st.selectbox('Ambulance starting location',STARTS)
    hospital=st.selectbox('Destination hospital',HOSPITALS)
    traffic=st.select_slider('Traffic scenario',['Low','Moderate','Heavy'],value='Moderate')
    st.caption('Traffic levels are simulated for the demonstration.')
    st.markdown('**Algorithm:** Dijkstra shortest path')

if start==hospital:
    st.error('Choose a starting location different from the hospital.'); st.stop()
G=build_graph(traffic); path,_=dijkstra(G,start,hospital,'minutes'); km,mins=stats(G,path)
# Generate a different simple route as a comparison where possible.
alt_options=[]
for p in nx.all_simple_paths(G,start,hospital,cutoff=7):
    if p!=path:
        akm,amin=stats(G,p); alt_options.append((amin,akm,p))
alt_options.sort(key=lambda x:(x[0],x[1])); alt=alt_options[0] if alt_options else None
st.subheader('Route Overview')
a,b,c,d=st.columns(4); a.metric('Estimated travel time',f'{mins} min'); b.metric('Route distance',f'{km:.1f} km'); c.metric('Locations in route',len(path)); d.metric('Traffic scenario',traffic)
left,right=st.columns([1.6,1])
with left:
    st.markdown('### Recommended Route Map'); st.pyplot(draw_graph(G,path,start,hospital),use_container_width=True); st.caption('Red: recommended route · Green: start · Yellow: destination')
with right:
    st.markdown('### Route Steps')
    for i,loc in enumerate(path):
        st.write(f'**{i+1}. {loc}**')
        if i<len(path)-1:
            edge=G[path[i]][path[i+1]]; st.caption(f"↳ {edge['distance']:.1f} km · about {edge['minutes']} min")
    st.success(f'Total: {km:.1f} km · {mins} minutes')
    if alt:
        am,ak,ap=alt; st.markdown('### Alternative Route'); st.write(' → '.join(ap)); st.caption(f'{ak:.1f} km · {am} min')
        st.info(f'Recommended route saves {am-mins} minute(s).' if am>mins else 'Alternative route is available for comparison.')

t1,t2,t3=st.tabs(['How Dijkstra Works','Compare Traffic','Project Details'])
with t1:
    st.markdown('#### Algorithm steps')
    st.markdown('1. Set the source cost to **0** and all other costs to infinity.\n2. Select the unvisited location with the lowest known cost using a priority queue.\n3. Check its neighbours and update costs when a better route is found.\n4. Repeat until the destination is reached.\n5. Trace previous locations to reconstruct the route.')
    st.code('''Dijkstra(G, source, destination):
    distance[source] = 0
    push (0, source) into priority queue
    while queue is not empty:
        cost, node = pop smallest item
        for each neighbour:
            new_cost = cost + edge_weight
            if new_cost < distance[neighbour]:
                update distance and previous node
                push updated cost into queue
    reconstruct path using previous nodes''')
    st.info("Time complexity with an adjacency list and binary heap: O((V + E) log V), where V is the number of vertices and E is the number of roads.")
with t2:
    rows=[]
    for level in ['Low','Moderate','Heavy']:
        sg=build_graph(level); sp,_=dijkstra(sg,start,hospital,'minutes'); sk,sm=stats(sg,sp)
        rows.append({'Traffic':level,'Route':' → '.join(sp),'Distance (km)':round(sk,1),'Estimated time (min)':sm})
    st.dataframe(rows,use_container_width=True,hide_index=True)
    st.caption('Sample comparison only; no live traffic is used.')
with t3:
    st.markdown('#### Problem statement')
    st.write('During an emergency, choosing an efficient route to a hospital is important. This prototype represents roads as a weighted graph and uses Dijkstra’s algorithm to find the route with the lowest estimated travel time.')
    st.markdown('#### Objectives')
    st.markdown('- Represent locations as vertices and roads as weighted edges.\n- Find a route using Dijkstra’s algorithm.\n- Compare route distance and simulated travel time.\n- Visualize the route and explain complexity.')
    st.markdown('#### Limitations')
    st.markdown('- Uses fictional sample locations and road distances.\n- Traffic is simulated, not live.\n- Not connected to GPS, hospitals, or emergency services.')
    st.markdown('#### Future scope')
    st.markdown('- Integrate a verified routing API and live traffic data.\n- Add road closures and more hospitals.\n- Add map-based location selection and route history.')
st.divider(); st.caption('EmergencyRoute · MCA DAA Mini Project · Python + Streamlit + NetworkX + Matplotlib')
