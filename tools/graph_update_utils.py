# -*- coding: utf-8 -*-
"""
Graf de Dades - Graph Update Utilities
======================================

Interactive widgets for updating the graph data through Jupyter Notebook.
Uses the new Python-native encryption modules.

Usage:
    1. Run the notebook cells in order
    2. Enter password and click "Desencripta!" to load data
    3. Add/modify nodes and edges using the widgets
    4. Click "Desa els canvis!" to save and encrypt

Authors:
    - Pau Matas (original)
    - Álvaro Domingo (maintainer)
"""

import ipywidgets as widgets
from IPython.display import display, clear_output
from datetime import datetime

# Import new modules
from tools.storage import load_graph_data, save_graph_data
from tools.models import Node, Edge, GraphData

# =============================================================================
# GLOBAL STATE
# =============================================================================

# Current graph data (loaded after decryption)
graph_data: GraphData = None

# Current password (needed for saving)
_current_password: str = None

# =============================================================================
# PASSWORD & LOAD/SAVE WIDGETS
# =============================================================================

password_widget = widgets.Password(
    placeholder='Contrassenya secreta',
    description='Password:',
    style={'description_width': 'initial'}
)

load_button = widgets.Button(
    description="🔓 Desencripta!",
    button_style='primary',
    tooltip='Carrega les dades encriptades'
)

save_button = widgets.Button(
    description="💾 Desa els canvis!",
    button_style='success',
    tooltip='Encripta i desa totes les dades'
)

output_area = widgets.Output()


def on_load_click(_):
    """Load and decrypt graph data."""
    global graph_data, _current_password
    
    with output_area:
        clear_output()
        try:
            _current_password = password_widget.value
            graph_data = load_graph_data(_current_password)
            print(f"✅ Desencriptat! Carregats {len(graph_data.nodes)} nodes i {len(graph_data.edges)} arestes")
            
            # Update all widgets with current data
            _update_node_widgets()
            _update_edge_widgets()
            _update_unwanted_widgets()
            
        except Exception as e:
            print(f"❌ Error: {e}")


def on_save_click(_):
    """Encrypt and save graph data."""
    global graph_data
    
    with output_area:
        clear_output()
        try:
            if graph_data is None:
                print("❌ No hi ha dades carregades!")
                return
                
            save_graph_data(graph_data, _current_password)
            print(f"✅ Desat! {len(graph_data.nodes)} nodes i {len(graph_data.edges)} arestes encriptades")
            print("📁 Backup creat a data/backups/")
            
        except Exception as e:
            print(f"❌ Error: {e}")


load_button.on_click(on_load_click)
save_button.on_click(on_save_click)


# =============================================================================
# NODE WIDGETS
# =============================================================================

node_name = widgets.Text(
    placeholder='Nom i cognoms',
    description='Nom:',
    style={'description_width': 'initial'}
)

node_year = widgets.BoundedIntText(
    value=datetime.now().year,
    min=2017,
    max=2030,
    description='Any entrada:',
    style={'description_width': 'initial'}
)

# Dynamic birth year helper
birth_year_label = widgets.HTML(value="")

def _update_birth_year_label(change):
    entry_year = change['new']
    # Born in year X typically enters university at year X+18
    birth_year = entry_year - 18
    birth_year_label.value = f"<i>🎂 Classe dels nascuts el <b>{birth_year}</b></i>"

node_year.observe(_update_birth_year_label, names='value')
# Trigger initial update
_update_birth_year_label({'new': node_year.value})

node_gender = widgets.Dropdown(
    options=[('Femení', 'F'), ('Masculí', 'M'), ('Altres', '-')],
    description='Gènere:',
    style={'description_width': 'initial'}
)

node_cfis = widgets.Checkbox(
    value=False,
    description='És CFIS?',
    indent=False
)

add_node_button = widgets.Button(
    description="➕ Afegeix node",
    button_style='info'
)

node_output = widgets.Output()


def _update_node_widgets():
    """Update node-related widgets after data changes."""
    pass  # Node widgets don't need dynamic updates


def _get_node_names() -> set:
    """Get all current node names."""
    if graph_data is None:
        return set()
    return graph_data.get_node_names()


def on_add_node_click(_):
    """Add a new node to the graph."""
    global graph_data
    
    with node_output:
        clear_output()
        
        name = node_name.value.strip()
        if not name:
            print("❌ El nom no pot estar buit!")
            return
            
        if name in _get_node_names():
            print(f"❌ El node '{name}' ja existeix!")
            return
        
        try:
            new_node = Node(
                label=name,
                year=node_year.value,
                gender=node_gender.value,
                cfis=node_cfis.value
            )
            graph_data.nodes.append(new_node)
            print(f"✅ Node '{name}' afegit correctament!")
            
            # Clear input
            node_name.value = ''
            
            # Update edge dropdowns
            _update_edge_widgets()
            _update_unwanted_widgets()
            
        except Exception as e:
            print(f"❌ Error: {e}")


add_node_button.on_click(on_add_node_click)


# =============================================================================
# EDGE WIDGETS
# =============================================================================

person1_dropdown = widgets.Dropdown(
    options=[],
    description='Persona 1:',
    style={'description_width': 'initial'}
)

person2_dropdown = widgets.Dropdown(
    options=[],
    description='Persona 2:',
    style={'description_width': 'initial'}
)

edge_weight = widgets.Dropdown(
    options=[('Lio', 1), ('Manual', 2), ('Oral', 3), ('Complert', 5)],
    value=1,
    description='Punts:',
    style={'description_width': 'initial'}
)

edge_place = widgets.Text(
    placeholder='On va passar?',
    description='Lloc:',
    style={'description_width': 'initial'}
)

# Month mapping for defaults
_month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
              7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

edge_month = widgets.Dropdown(
    options=[
        ('Gener', 'Jan'), ('Febrer', 'Feb'), ('Març', 'Mar'),
        ('Abril', 'Apr'), ('Maig', 'May'), ('Juny', 'Jun'),
        ('Juliol', 'Jul'), ('Agost', 'Aug'), ('Setembre', 'Sep'),
        ('Octubre', 'Oct'), ('Novembre', 'Nov'), ('Desembre', 'Dec'),
        ('Desconegut', '')
    ],
    value=_month_map.get(datetime.now().month, ''),
    description='Mes:',
    style={'description_width': 'initial'}
)

edge_year = widgets.BoundedIntText(
    value=datetime.now().year,
    min=2017,
    max=2030,
    description='Any:',
    style={'description_width': 'initial'}
)

edge_repeated = widgets.Checkbox(
    value=False,
    description='Van repetir?',
    indent=False
)

edge_relationship = widgets.Checkbox(
    value=False,
    description='Tenen/han tingut relació?',
    indent=False
)

edge_comments = widgets.Text(
    placeholder='Comentaris opcionals...',
    description='Comentaris:',
    style={'description_width': 'initial'}
)

edge_remove = widgets.Checkbox(
    value=False,
    description='🗑️ ELIMINAR aresta existent',
    indent=False,
    style={'description_width': 'initial'}
)

add_edge_button = widgets.Button(
    description="➕ Afegeix/Modifica aresta",
    button_style='info'
)

edge_output = widgets.Output()


def _update_edge_widgets():
    """Update edge-related widgets after data changes."""
    names = sorted(_get_node_names())
    person1_dropdown.options = names
    person2_dropdown.options = names


def _find_edge(source: str, target: str):
    """Find an existing edge between two people."""
    if graph_data is None:
        return None, None
    
    for i, e in enumerate(graph_data.edges):
        if (e.source == source and e.target == target) or \
           (e.source == target and e.target == source):
            return i, e
    return None, None


def on_add_edge_click(_):
    """Add or update an edge."""
    global graph_data
    
    with edge_output:
        clear_output()
        
        p1 = person1_dropdown.value
        p2 = person2_dropdown.value
        
        if p1 == p2:
            print("❌ Les dues persones han de ser diferents!")
            return
        
        idx, existing = _find_edge(p1, p2)
        
        if edge_remove.value:
            # Delete edge
            if existing is None:
                print(f"❌ No existeix cap aresta entre '{p1}' i '{p2}'")
            else:
                graph_data.edges.pop(idx)
                print(f"🗑️ Aresta entre '{p1}' i '{p2}' eliminada!")
                edge_remove.value = False
        
        elif existing is not None:
            # Update existing edge
            existing.weight = edge_weight.value
            existing.repeated = edge_repeated.value
            existing.relationship = edge_relationship.value
            print(f"✏️ Aresta entre '{p1}' i '{p2}' actualitzada!")
        
        else:
            # Create new edge
            try:
                new_edge = Edge(
                    source=p1,
                    target=p2,
                    weight=edge_weight.value,
                    place=edge_place.value,
                    month=edge_month.value,
                    year=edge_year.value,
                    repeated=edge_repeated.value,
                    relationship=edge_relationship.value,
                    comments=edge_comments.value or None
                )
                graph_data.edges.append(new_edge)
                print(f"✅ Aresta entre '{p1}' i '{p2}' afegida!")
                
                # Clear inputs
                edge_place.value = ''
                edge_comments.value = ''
                
            except Exception as e:
                print(f"❌ Error: {e}")


add_edge_button.on_click(on_add_edge_click)


# =============================================================================
# ANONYMIZATION WIDGETS
# =============================================================================

unwanted_dropdown = widgets.Dropdown(
    options=[],
    description='Persona:',
    style={'description_width': 'initial'}
)

anonymize_button = widgets.Button(
    description="👤 Anonimitza",
    button_style='warning',
    tooltip='La persona apareixerà com "Anònim X" al graf'
)

unwanted_output = widgets.Output()


def _update_unwanted_widgets():
    """Update unwanted-related widgets after data changes."""
    if graph_data is None:
        return
    
    # Show only non-anonymized people
    already_unwanted = set(graph_data.unwanted)
    available = sorted(_get_node_names() - already_unwanted)
    unwanted_dropdown.options = available


def on_anonymize_click(_):
    """Add a person to the unwanted list."""
    global graph_data
    
    with unwanted_output:
        clear_output()
        
        person = unwanted_dropdown.value
        if not person:
            print("❌ Selecciona una persona!")
            return
        
        if person in graph_data.unwanted:
            print(f"❌ '{person}' ja està anonimitzat!")
            return
        
        graph_data.unwanted.append(person)
        print(f"✅ '{person}' serà anonimitzat com 'Anònim' al graf públic")
        
        _update_unwanted_widgets()


anonymize_button.on_click(on_anonymize_click)


# =============================================================================
# EDGE SEARCH/MODIFY WIDGETS (separate from add)
# =============================================================================

search_person1 = widgets.Dropdown(
    options=[],
    description='Persona 1:',
    style={'description_width': 'initial'}
)

search_person2 = widgets.Dropdown(
    options=[],
    description='Persona 2:',
    style={'description_width': 'initial'}
)

search_button = widgets.Button(
    description="🔍 Buscar aresta",
    button_style='info'
)

modify_weight = widgets.Dropdown(
    options=[('Lio', 1), ('Manual', 2), ('Oral', 3), ('Complert', 5)],
    value=1,
    description='Punts:',
    style={'description_width': 'initial'}
)

modify_year = widgets.BoundedIntText(
    value=datetime.now().year,
    min=2017,
    max=2030,
    description='Any:',
    style={'description_width': 'initial'}
)

modify_month = widgets.Dropdown(
    options=[
        ('Gener', 'Jan'), ('Febrer', 'Feb'), ('Març', 'Mar'),
        ('Abril', 'Apr'), ('Maig', 'May'), ('Juny', 'Jun'),
        ('Juliol', 'Jul'), ('Agost', 'Aug'), ('Setembre', 'Sep'),
        ('Octubre', 'Oct'), ('Novembre', 'Nov'), ('Desembre', 'Dec'),
        ('Desconegut', '')
    ],
    description='Mes:',
    style={'description_width': 'initial'}
)

modify_repeated = widgets.Checkbox(
    value=False,
    description='Van repetir?',
    indent=False
)

modify_relationship = widgets.Checkbox(
    value=False,
    description='Tenen/han tingut relació?',
    indent=False
)

modify_place = widgets.Text(
    placeholder='On va passar?',
    description='Lloc:',
    style={'description_width': 'initial'}
)

modify_comments = widgets.Text(
    placeholder='Comentaris...',
    description='Comentaris:',
    style={'description_width': 'initial'}
)

modify_button = widgets.Button(
    description="✏️ Modificar",
    button_style='warning'
)

delete_button = widgets.Button(
    description="🗑️ Eliminar",
    button_style='danger'
)

search_output = widgets.Output()


def _update_search_widgets():
    """Update search dropdowns."""
    names = sorted(_get_node_names())
    search_person1.options = names
    search_person2.options = names


def on_search_click(_):
    """Search for an edge."""
    with search_output:
        clear_output()
        
        p1 = search_person1.value
        p2 = search_person2.value
        
        if not p1 or not p2:
            print("❌ Selecciona les dues persones")
            return
        
        idx, edge = _find_edge(p1, p2)
        
        if edge is None:
            print(f"❌ No existeix cap aresta entre '{p1}' i '{p2}'")
        else:
            print(f"✅ Aresta trobada!")
            print(f"   Punts: {edge.weight}")
            print(f"   Lloc: {edge.place or 'N/A'}")
            print(f"   Data: {edge.month or '?'} {edge.year or '?'}")
            print(f"   Repetit: {'Sí' if edge.repeated else 'No'}")
            print(f"   Relació: {'Sí' if edge.relationship else 'No'}")
            if edge.comments:
                print(f"   Comentaris: {edge.comments}")
            
            # Pre-fill modify widgets
            modify_weight.value = edge.weight
            if edge.year:
                modify_year.value = edge.year
            if edge.month:
                modify_month.value = edge.month
            modify_repeated.value = edge.repeated
            modify_relationship.value = edge.relationship
            modify_place.value = edge.place or ''
            modify_comments.value = edge.comments or ''


def on_modify_click(_):
    """Modify an existing edge."""
    global graph_data
    
    with search_output:
        clear_output()
        
        p1 = search_person1.value
        p2 = search_person2.value
        idx, edge = _find_edge(p1, p2)
        
        if edge is None:
            print(f"❌ No existeix cap aresta entre '{p1}' i '{p2}'")
        else:
            edge.weight = modify_weight.value
            edge.year = modify_year.value
            edge.month = modify_month.value
            edge.repeated = modify_repeated.value
            edge.relationship = modify_relationship.value
            edge.place = modify_place.value or ''
            edge.comments = modify_comments.value or None
            print(f"✅ Aresta entre '{p1}' i '{p2}' actualitzada!")


def on_delete_click(_):
    """Delete an edge."""
    global graph_data
    
    with search_output:
        clear_output()
        
        p1 = search_person1.value
        p2 = search_person2.value
        idx, edge = _find_edge(p1, p2)
        
        if edge is None:
            print(f"❌ No existeix cap aresta entre '{p1}' i '{p2}'")
        else:
            graph_data.edges.pop(idx)
            print(f"🗑️ Aresta entre '{p1}' i '{p2}' eliminada!")


search_button.on_click(on_search_click)
modify_button.on_click(on_modify_click)
delete_button.on_click(on_delete_click)


# =============================================================================
# DISPLAY HELPERS (for notebook)
# =============================================================================

def show_load_section():
    """Display the password and load/save section."""
    return widgets.VBox([
        widgets.HTML("<h2>🔐 Carregar Dades</h2>"),
        password_widget,
        widgets.HBox([load_button, save_button]),
        output_area
    ])


def show_node_section():
    """Display the add node section with vertical layout and birth year helper."""
    return widgets.VBox([
        widgets.HTML("<h2>👤 Afegir Node (Persona)</h2>"),
        node_name,
        node_year,
        birth_year_label,
        node_gender,
        node_cfis,
        add_node_button,
        node_output
    ])


def show_edge_search_section():
    """Display the edge search/modify/delete section."""
    # Update dropdowns
    _update_search_widgets()
    
    return widgets.VBox([
        widgets.HTML("<h2>🔍 Buscar / Modificar / Eliminar Aresta</h2>"),
        widgets.HBox([search_person1, search_person2]),
        search_button,
        widgets.HTML("<hr><b>Modificar:</b>"),
        widgets.HBox([modify_year, modify_month]),
        modify_weight,
        modify_place,
        widgets.HBox([modify_repeated, modify_relationship]),
        modify_comments,
        widgets.HBox([modify_button, delete_button]),
        search_output
    ])


def show_edge_add_section():
    """Display the add new edge section."""
    return widgets.VBox([
        widgets.HTML("<h2>➕ Afegir Nova Aresta</h2>"),
        # Row 1: Persons
        widgets.HBox([person1_dropdown, person2_dropdown]),
        # Row 2: Year, Month
        widgets.HBox([edge_year, edge_month]),
        # Row 3: Points
        edge_weight,
        # Row 4: Place
        edge_place,
        # Row 5: Other fields
        edge_repeated,
        edge_relationship,
        # Row 6: Comments
        edge_comments,
        # Button
        add_edge_button,
        edge_output
    ])


def show_anonymize_section():
    """Display the anonymization section."""
    return widgets.VBox([
        widgets.HTML("<h2>🕵️ Anonimitzar Persona</h2>"),
        widgets.HTML("<p><em>La persona apareixerà com 'Anònim X' al graf públic.</em></p>"),
        unwanted_dropdown,
        anonymize_button,
        unwanted_output
    ])


# Legacy compatibility
def show_edge_section():
    """Legacy: shows both edge sections in tabs."""
    return widgets.Tab(children=[
        show_edge_add_section(),
        show_edge_search_section()
    ], titles=['➕ Afegir', '🔍 Buscar/Modificar'])


# =============================================================================
# CONVENIENCE EXPORTS
# =============================================================================

password = password_widget
decrypt_button = load_button
end_button = save_button

def get_persons():
    """Legacy function for edge widget dropdowns."""
    return person1_dropdown, person2_dropdown, unwanted_dropdown

