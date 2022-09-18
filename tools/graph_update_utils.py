# -*- graph_update_utils.py -*-

"""
Python script designed to provide features to a .ipynb file able to update the
graph raw data (nodes, edges and unwanted nodes) with less code as possible.
"""

# Built-in/Generic Imports
import os

# Libs
import pandas as pd
import json
import ipywidgets as widgets

__author__ = 'Pau Matas'
__maintainer__ = 'Pau Matas'
__email__ = 'pmatasalbiol@gmail.com'
__status__ = 'Dev'

# Working directory setting
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Data
node_names, current_edges = None, None # Global vars

with open('./../data/raw_nodes.json') as json_file:
    nodes = json.load(json_file)

with open('./../data/raw_edges.json') as json_file:
    edges = json.load(json_file)

with open('./../data/unwanted.json') as json_file:
    unwanted = json.load(json_file)

# Node tools

person = widgets.Text(
    placeholder='Com es diu?',
    description='Nom:',
    disabled=False
)

gender = widgets.Dropdown(
    options=[('Femení', 'F'), ('Masculí', 'M'), ('Altres', '-')],
    description='Sexe: ',
)

node_year = widgets.BoundedIntText(
    min=2017,
    max=2030,
    step=1,
    description='Any: ',
    disabled=False
)

cfis = widgets.Checkbox(
    value=False,
    description='És CFIS?',
    disabled=False,
    indent=True
)

node_button = widgets.Button(description="Afegeix el node!", indent=True)

def node_mutable_widgets():
    """ Redefines the mutable node related widgets"""

    global nodes_names
    nodes_names = {n['label'] for n in nodes}

node_mutable_widgets()

def add_node(_):
    """ Adds the node specified on the widgets to the graph raw data files """

    global nodes

    if person.value in nodes_names or person.value == '':
        raise Exception('This node already exists')

    nodes.append({
        "label": person.value,
        "year": node_year.value,
        "gender": gender.value,
        "cfis": str(cfis.value).upper()
    })

    with open('./../data/raw_nodes.json', 'w') as json_file:
        json.dump(nodes, json_file, ensure_ascii=False, indent=2)

    print(f'S\'ha afegit el node \"{person.value}\" correctament')

    node_mutable_widgets()
    edge_mutable_widgets()

node_button.on_click(add_node)

# Edge tools

person1, person2 = None, None

points = widgets.Dropdown(
    options=[('Lio', 1),('Manual', 2), ('Oral', 3), ('Complert', 5)],
    value=1,
    description='Punts: ',
)

location = widgets.Text(
    placeholder='On va passar?',
    description='Lloc:',
    disabled=False
)

month = widgets.Dropdown(
    options=[('Gener', 'Jan'), ('Febrer', 'Feb'), ('Març', 'Mar'), ('Abril', 'Apr'), ('Maig', 'May'),
             ('Juny', 'Jun'), ('Juliol', 'Jul'), ('Agost', 'Aug'), ('Setembre', 'Sep'),
             ('Octubre', 'Oct'), ('Novembre', 'Nov'), ('Desembre', 'Dec'),('Unknown', '')],
    description='Mes:',
)

edge_year = widgets.BoundedIntText(
    min=2017,
    max=2025,
    step=1,
    description='Any:',
    disabled=False
)

repetition = widgets.Checkbox(
    value=False,
    description='Van repetir?',
    disabled=False,
    indent=True
)

relationship = widgets.Checkbox(
    value=False,
    description='Tenen o han tingut una relació?',
    disabled=False,
    indent=True
)

edge_button = widgets.Button(description="Afegeix l'aresta!", indent=True)

def edge_mutable_widgets():
    """ Redefines the mutable edge related widgets"""

    global current_edges
    global person1
    global person2

    current_edges = [{e['source'], e['target']} for e in edges]

    person1 = widgets.Dropdown(
        options=list(sorted(nodes_names)),
        description='Person 1:',
    )

    person2 = widgets.Dropdown(
        options=list(sorted(nodes_names)),
        description='Person 2:',
    )

edge_mutable_widgets()

def update_edge():
    """ Updates the edge updatable attributes with the specified ones on
        the widgets
    """
    global edges

    for i, e in enumerate(edges):
        if ((e['source'] == person1.value and e['target'] == person2.value) or
            (e['source'] == person2.value and e['target'] == person1.value)):

            edges[i]["weight"] = points.value
            edges[i]["repeated"] = str(repetition.value).upper()
            edges[i]["relationship"] = str(relationship.value).upper()

            break

def add_edge(_):
    """ Adds or updates the edge specified on the widgets on the graph raw
        data files
    """

    global edges

    if person1.value == person2.value:
        raise Exception('Both persons need to be different')

    if {person1.value, person2.value} in current_edges:
        update_edge()

    else:
        edges.append({
            "source": person1.value,
            "target": person2.value,
            "weight": points.value,
            "place": location.value,
            "month": month.value,
            "year": edge_year.value,
            "repeated": str(repetition.value).upper(),
            "relationship": str(relationship.value).upper()
        })

    with open('./../data/raw_edges.json', 'w') as json_file:
        json.dump(edges, json_file, ensure_ascii=False, indent=2)

    print(f'La aresta entre els nodes \"{person1.value}\" i \"{person2.value}\" ha estat afegida amb èxit')

    edge_mutable_widgets()


edge_button.on_click(add_edge)

# Unwanted tools

wanted, unwanted_person = None, None

def unwanted_mutable_widgets():
    """ Redefines the mutable unwanted nodes related widgets"""

    global unwanted_person
    global wanted

    wanted = nodes_names.difference(unwanted)

    unwanted_person = widgets.Dropdown(
        options=list(sorted(wanted)),
        description='Nom: ',
    )

unwanted_mutable_widgets()

unwanted_button = widgets.Button(description="Anonimitza el node...")

def add_unwanted(_):
    """ Adds the node specified on the widget to unwanted.json data file """

    unwanted['unwanted'].append(unwanted_person.value)

    with open('./../data/unwanted.json', 'w') as json_file:
        json.dump(unwanted, json_file, ensure_ascii=False, indent=2)

    print(f'S\'ha anonimitzat el node \"{unwanted_person.value}\" correctament')

    unwanted_mutable_widgets()

unwanted_button.on_click(add_unwanted)
