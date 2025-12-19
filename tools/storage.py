# -*- coding: utf-8 -*-
"""
File storage operations for Graf de Dades.
Handles loading, saving, and backup of encrypted graph data.
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

from .models import GraphData, Node, Edge
from .crypto import encrypt, decrypt


# Default paths
DATA_DIR = Path(__file__).parent.parent / "data"
BACKUP_DIR = DATA_DIR / "backups"

# File names
GRAPH_DATA_FILE = "graph_data.enc"           # New single source of truth
FRONTEND_DATA_FILE = "encrypted_data.txt"    # For browser consumption

# Legacy files (for migration)
LEGACY_NODES_FILE = "encrypted_nodes.txt"
LEGACY_EDGES_FILE = "encrypted_edges.txt"
LEGACY_UNWANTED_FILE = "encrypted_unwanted.txt"


def ensure_dirs() -> None:
    """Ensure data and backup directories exist."""
    DATA_DIR.mkdir(exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)


def create_backup(filename: str) -> Optional[Path]:
    """
    Create a timestamped backup of a file.
    
    Args:
        filename: Name of file in DATA_DIR to backup
    
    Returns:
        Path to backup file, or None if source doesn't exist
    """
    ensure_dirs()
    source = DATA_DIR / filename
    if not source.exists():
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{source.stem}_{timestamp}{source.suffix}"
    backup_path = BACKUP_DIR / backup_name
    shutil.copy2(source, backup_path)
    return backup_path


def load_graph_data(password: str, use_legacy: bool = False) -> GraphData:
    """
    Load and decrypt graph data from storage.
    
    Args:
        password: Decryption password
        use_legacy: If True, load from legacy separate files
    
    Returns:
        GraphData object with all nodes, edges, and unwanted list
    """
    if use_legacy:
        return _load_legacy(password)
    
    filepath = DATA_DIR / GRAPH_DATA_FILE
    encrypted = filepath.read_text(encoding="utf-8")
    decrypted = decrypt(encrypted, password)
    data = json.loads(decrypted)
    
    return GraphData(
        nodes=[Node(**n) for n in data.get("nodes", [])],
        edges=[Edge(**e) for e in data.get("edges", [])],
        unwanted=data.get("unwanted", [])
    )


def _load_legacy(password: str) -> GraphData:
    """Load from legacy separate encrypted files."""
    from .crypto import decrypt
    
    # Load nodes
    nodes_file = DATA_DIR / LEGACY_NODES_FILE
    if nodes_file.exists():
        encrypted = nodes_file.read_text(encoding="utf-8")
        nodes_data = json.loads(decrypt(encrypted, password, use_legacy=True))
        nodes = [Node(**n) for n in nodes_data]
    else:
        nodes = []
    
    # Load edges
    edges_file = DATA_DIR / LEGACY_EDGES_FILE
    if edges_file.exists():
        encrypted = edges_file.read_text(encoding="utf-8")
        edges_data = json.loads(decrypt(encrypted, password, use_legacy=True))
        edges = [Edge(**e) for e in edges_data]
    else:
        edges = []
    
    # Load unwanted
    unwanted_file = DATA_DIR / LEGACY_UNWANTED_FILE
    if unwanted_file.exists():
        encrypted = unwanted_file.read_text(encoding="utf-8")
        unwanted_data = json.loads(decrypt(encrypted, password, use_legacy=True))
        unwanted = unwanted_data.get("unwanted", [])
    else:
        unwanted = []
    
    return GraphData(nodes=nodes, edges=edges, unwanted=unwanted)


def save_graph_data(data: GraphData, password: str, backup: bool = True) -> None:
    """
    Encrypt and save graph data.
    
    Args:
        data: GraphData to save
        password: Encryption password
        backup: If True, create backup before overwriting
    """
    ensure_dirs()
    
    if backup:
        create_backup(GRAPH_DATA_FILE)
        create_backup(FRONTEND_DATA_FILE)
    
    # Assign IDs
    data.assign_ids()
    
    # Save main data file (source of truth)
    main_data = {
        "nodes": [n.model_dump() for n in data.nodes],
        "edges": [e.model_dump() for e in data.edges],
        "unwanted": data.unwanted
    }
    encrypted = encrypt(json.dumps(main_data, ensure_ascii=False, indent=2), password)
    (DATA_DIR / GRAPH_DATA_FILE).write_text(encrypted, encoding="utf-8")
    
    # Save frontend file (anonymized, legacy format)
    frontend_data = data.to_frontend_dict()
    frontend_encrypted = encrypt(
        json.dumps(frontend_data, ensure_ascii=False), 
        password, 
        use_legacy=True  # Frontend still uses legacy decryption
    )
    (DATA_DIR / FRONTEND_DATA_FILE).write_text(frontend_encrypted, encoding="utf-8")


def migrate_from_legacy(password: str) -> GraphData:
    """
    Migrate from legacy storage format to new format.
    
    Args:
        password: The encryption password
    
    Returns:
        Migrated GraphData
    """
    # Load from legacy files
    data = _load_legacy(password)
    
    # Create backups of legacy files
    create_backup(LEGACY_NODES_FILE)
    create_backup(LEGACY_EDGES_FILE)
    create_backup(LEGACY_UNWANTED_FILE)
    
    # Save in new format
    save_graph_data(data, password, backup=False)
    
    return data
