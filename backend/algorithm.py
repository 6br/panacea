import forceatlas2
from pyvis.network import Network
import networkx as nx
import requests
import pydot
from collections import defaultdict

MEDIA_KEYS = ["candidate", "person"]
HOST = "http://x2:3000"
COLOR_SET = ["#f7a700", "#fff100", "#804000", "#FF4B00", "#84919e", "#c8c8cb"]
NORMAL_COLOR = '#77d9a8'
SIZE_SCALING = 20

def query(source, target, year, scale, offset):
    #print(scale)
    query = """ \
    MATCH (n:{source})-[e]-(m)
    WITH n, count(*) AS cc
    ORDER BY cc DESC
    SKIP {offset}
    LIMIT {limit}
    MATCH (n:{source})<-[e1]-(t:{medium})-[e2]->(k:{target}) 
    WHERE t.year = {year}
    RETURN n,e1,t,e2,k LIMIT 3000
    """.format(year=year, source=source, target=target, medium=MEDIA_KEYS[0], limit=scale, offset=offset)

    res = requests.get('{host}/query/'.format(host=HOST), params={"q": query, "raw": "true"})
    res.raise_for_status()
    result = res.json()['pg']
    raw = res.json()['raw']
    return result, raw

def node_query(node_labels):
    if len(node_labels) == 1:
        query = """
        MATCH (n:{node_label})
        RETURN n
        """.format(node_label=node_labels[0])
        res = requests.get('{host}/query/'.format(host=HOST), params={"q": query, "raw": "true"})
        res.raise_for_status()
        raw = res.json()['raw']
        return raw
    elif len(node_labels) == 2:
        res = requests.get('{host}/node_match?node_labels[]={node_id1}&node_labels[]={node_id2}'.format(host=HOST, node_id1=node_labels[0], node_id2=node_labels[1]), params={"raw": "true"})
        res.raise_for_status()
        return res.json()

def edge_query(edge_label):
        query = """
        MATCH (n)-[r:{edge_label}]-(m)
        RETURN *
        """.format(node_label=node_labels[0])
        res = requests.get('{host}/query/'.format(host=HOST), params={"q": query, "raw": "true"})
        res.raise_for_status()
        raw = res.json()['raw']
        return raw

def media_query(media_id):
    res = requests.get('{host}/traversal/?node_ids={node_id}&iteration=2'.format(host=HOST, node_id=media_id), params={"raw": "true"})
    res.raise_for_status()
    return res.json()
#    query = """ \
#    MATCH (n)<-[e1]-(t) 
#    WHERE t.id = {medium}
#    RETURN n,e1,t LIMIT 3000
#    """.format(medium=media_id)

#    res = requests.get('{host}/query/'.format(host=HOST), params={"q": query, "raw": "true"})
#    result = res.json()['pg']
#    raw = res.json()['raw']
#    return result

def table_query(source, target, scale):
    query = """
    MATCH (n:{source})-[e]-(m)
    WITH n, count(*) AS cc
    ORDER BY cc DESC
    LIMIT {limit}
    MATCH (n:{source})<-[e1]-(t:{medium})-[e2]->(k:{target}) 
    WITH t.year AS year, n.name AS source, count(*) as cc
    ORDER BY year ASC
    RETURN source, year, cc
    """.format(source=source, target=target, medium=MEDIA_KEYS[0], limit = scale)
    res = requests.get('{host}/query/'.format(host=HOST), params={"q": query, "raw": "true"})
    res.raise_for_status()
    raw = res.json()['raw']
    return raw

def count_num_query(source, target, year):
    query = """ \
    MATCH (n:{source})-[e]-(m)
    WITH n, count(*) AS cc
    ORDER BY cc DESC
    LIMIT 12
    MATCH (n:{source})<-[e1]-(t:{medium})-[e2]->(k:{target}) 
    WHERE t.year = {year}
    WITH count(distinct(n)) AS cn, count(distinct(k)) as ck
    RETURN cn, ck
    """.format(year=year, source=source, target=target, medium=MEDIA_KEYS[0])
    res = requests.get('{host}/query/'.format(host=HOST), params={"q": query, "raw": "true"})
    res.raise_for_status()
    raw = res.json()['raw']['results'][0]['data'][0]['row']
    if int(raw[0]) <= int(raw[1]):
        return source, target
    else:
        return target, source

def profile_query(prof_type):
    res = requests.get('{host}/profile'.format(host=HOST), params={"type": prof_type, "raw": "true"})
    res.raise_for_status()
    return res.json()
    
def forceatlas(result, pos, edges, niter=100):
    NX = nx.Graph()
    node_name = { d['id']: d['id'] for d in result['nodes']}
    NX.add_nodes_from(node_name.keys())
    NX.add_edges_from([(x['from'], x['to']) for x in edges])
    pos = forceatlas2.forceatlas2_networkx_layout(NX, pos, niter=niter)
    return pos

def to_bipertite_edges(raw):
    ret_list = []
    for item in raw['results'][0]['data']:
        ret_list.append({"from": str(item['meta'][0]['id']), "to": str(item['meta'][4]['id'])})
    return ret_list

def create_network(result, pos, edges, source, target, simple=False, auto=False, english=False, dark=False):
    k = {}
    index = 0
    node_name = { d['id']: d['id'] for d in result['nodes'] if 'name'}
    if not dark:
        G = Network(notebook=True, height="700px", width="100%", directed=True, layout=False, bgcolor="#ffffff", font_color="black")
    else:
        G = Network(notebook=True, height="700px", width="100%", directed=True, layout=False, bgcolor="#222222", font_color="white")
    # https://jfly.uni-koeln.de/colorset/CUD_color_set_GuideBook_2018.pdf
    edge_dict = defaultdict(list)
    for d in edges:
        edge_dict[d['from']].append(d['to'])
    for d in result['nodes']:
        v = node_name[d['id']]
        if simple:
            v_d = {'color': NORMAL_COLOR, 'size': 100, 'physics': True}
        else:
            x, y = pos[d['id']]
            v_d = {'color': NORMAL_COLOR, 'size': 100, 'physics': True, 'x': x * SIZE_SCALING, 'y': y * SIZE_SCALING}

        if "name" in d['properties'] and not english:
            v_d["label"] = d['properties']['name']
        elif english: # no_label
            v_d["label"] = " "
        if edge_dict[d['id']]:
            v_d["attr"] = sorted(edge_dict[d['id']])
        if source in d['labels']:
            # Primary Node
            v_d["color"] = "#00A5FF"
            x, y = pos[d['id']]
            v_d["physics"] = False
            v_d["x"] = x * SIZE_SCALING
            v_d["y"] = y * SIZE_SCALING
            v_d["shape"] = "square"
        elif target in d['labels']:
            v_d["color"] = '#f7a700'
            v_d["shape"] = "triangle"
            if english:
                v_d["color"] = COLOR_SET[int(d['id']) % len(COLOR_SET)]
        else:
            v_d["size"] = 25
            v_d["label"] = " "
            v_d["node_id"] = d['id']

        G.add_node(v, **v_d)
    for d in edges:
        try:
            u, v = node_name[d['from']], node_name[d['to']]
            e_d = {"value": 3}
            G.add_edge(u, v, **e_d)
        except Exception as e:
            print(sys.exc_info())
            pass
    return G

"""
def create_simple_network(result, pos, edges, source, target):
    k = {}
    index = 0
    node_name = { d['id']: d['id'] for d in result['nodes'] if 'name'}
    G = Network(notebook=True, height="700px", width="100%", directed=True, layout=False, bgcolor="#222222", font_color="white")
    edge_dict = defaultdict(list)
    for d in edges:
        edge_dict[d['from']].append(d['to'])
    for d in result['nodes']:
        v = node_name[d['id']]
        v_d = {'color': '#DFA06E', 'size': 100, 'physics': True}
        if "name" in d['properties']:
            v_d["label"] = d['properties']['name']
        if edge_dict[d['id']]:
            v_d["attr"] = edge_dict[d['id']]
        if source in d['labels']:
            v_d["color"] = "#148487"
            x, y = pos[d['id']]
            v_d["physics"] = False
            v_d["x"] = x * 30
            v_d["y"] = y * 30
        elif target in d['labels']:
            v_d["color"] = '#86BA90'
        else:
            v_d["size"] = 10
            v_d["label"] = " "

        G.add_node(v, **v_d)
    for d in edges:
        try:
            u, v = node_name[d['from']], node_name[d['to']]
            e_d = {"value": 3}
            G.add_edge(u, v, **e_d)
        except Exception as e:
            print(sys.exc_info())
            pass
    return G
"""
def star_layout(G):
    nodes = list(G.nodes)
    g = G.subgraph(nodes[1:])
    pos = nx.circular_layout(g, center=(1, 1))
    if len(nodes) > 0:
        pos[nodes[0]] = (1, 1)
    return pos

def star_prime_layout(G):
    nodes = list(G.nodes)
    if len(nodes) == 0:
        return {}
    close_centers = nx.closeness_centrality(G)
    close_center_nodeid = sorted(close_centers.items(), key=lambda x: x[1], reverse=True)[0][0]
    nodes.remove(close_center_nodeid)
    
    g = G.subgraph(nodes)
    pos = nx.circular_layout(g, center=(1, 1))
    pos[close_center_nodeid] = (1, 1)
    return pos
    

def tree_layout(G):
    pos = nx.nx_pydot.graphviz_layout(G, prog='dot')
    pos = {k: (x / 96, y / 96) for k, (x, y) in pos.items()}
    return pos


def fetch(first, second, year, inherit, auto, layout, scale, english, dark, offset):
    if auto:
        first, second = count_num_query(first, second, year)
    result, raw = query(first, second, year, scale, offset)
    edges = to_bipertite_edges(raw)
    NX = nx.Graph()
    NX.add_nodes_from([ x['from'] for x in edges])
    if layout == "linear":
        NX.add_nodes_from([ x['to'] for x in edges])
        NX.add_edges_from([ (x['from'], x['to']) for x in edges])
        pos4 = nx.bipartite_layout(NX, [ x['id'] for x in result['nodes'] if first in x["labels"] ], align='horizontal' )
        pos3 = {}
        for k,v in pos4.items():
            if k in [ x['id'] for x in result['nodes'] if first in x["labels"] ]:
                pos3[k] = (v[0], v[1])
    elif layout == "star":
        pos3 = star_layout(NX)
    elif layout == "star'":
        pos3 = star_prime_layout(NX)
    elif layout == "tree" or layout == "spatial":
        pos3 = tree_layout(NX)
    else: 
        pos3 = nx.circular_layout(NX) #, [ x['id'] for x in result['nodes'] if "university" in x["labels"] ] , align='vertical')

    pos2 = {}
    for k in [ x['to'] for x in edges]:
        pos2[k] = (0,0)
    for k,v in pos3.items():
        pos2[k] = (v[0] * 100, v[1] * 100)


    if inherit:
        G = create_network(result, pos2, result['edges'], first, second, True, auto, english, dark)
        nodes, edges, height, width, options = G.get_network_data()
        return result, pos2, nodes, edges, height, width, options

    #print(pos2)
    pos = forceatlas(result, pos2, result['edges'], 0);
    #print(pos)
    G = create_network(result, pos, result['edges'], first, second, False, auto, english, dark)
    G.force_atlas_2based(-100, 0)
    G.options.physics["stabilization"].iterations = 100
    #G.show_buttons(filter_=['physics'])
    #G.show_buttons(filter_=True)
    nodes, edges, height, width, options = G.get_network_data()

    return result, pos, nodes, edges, height, width, options

