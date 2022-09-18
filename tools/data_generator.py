import json

DATA_PATH = './../data'

def generate():
    # Opening JSON file
    with open(f'{DATA_PATH}/decrypted_nodes.json') as json_file:
        nodes = json.load(json_file)

    with open(f'{DATA_PATH}/decrypted_edges.json') as json_file:
        edges = json.load(json_file)

    with open(f'{DATA_PATH}/decrypted_unwanted.json') as json_file:
        unwanted = set(json.load(json_file)['unwanted'])

    nodes_names = {n['label'] for n in nodes}

    unwanted_mapping = {unw: f'Anònim {i}' for i, unw in enumerate(unwanted)}

    if len(nodes_names) != len(nodes):
        print(len(nodes_names))
        print(len(nodes))
        raise('Repeated nodes')



    consistent = True
    for edge in edges:
        if not edge['source'] in nodes_names:
            print(edge['source'])
            consistent = False
        if not edge['target'] in nodes_names:
            print(edge['target'])
            consistent = False

    if consistent:
        graph_nodes = []

        for n in nodes:
            if n['label'] in unwanted:
                n['label'] = unwanted_mapping[n['label']]
            graph_nodes.append(n)

        for i,n in enumerate(graph_nodes):
            n['id'] = i

        graph_edges = []
        for e in edges:
            if e['source'] in unwanted:
                e['source'] = unwanted_mapping[e['source']]

            if e['target'] in unwanted:
                e['target'] = unwanted_mapping[e['target']]

            graph_edges.append(e)

        for i,e in enumerate(graph_edges):
            e['id'] = i

        data = {'edges': graph_edges, 'nodes': graph_nodes}
        with open(f'{DATA_PATH}/decrypted_data.json', 'w') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)
