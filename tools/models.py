# -*- coding: utf-8 -*-
"""
Data models for Graf de Dades with Pydantic validation.
"""

from typing import Literal, Optional
from pydantic import BaseModel, field_validator, model_validator


class Node(BaseModel):
    """A person in the graph."""
    id: Optional[int] = None
    label: str
    year: int
    gender: Literal["F", "M", "-"]
    cfis: bool

    @field_validator("year")
    @classmethod
    def validate_year(cls, v: int) -> int:
        if not 2017 <= v <= 2100:
            raise ValueError(f"Year must be between 2017 and 2100, got {v}")
        return v

    @field_validator("cfis", mode="before")
    @classmethod
    def parse_cfis(cls, v):
        if isinstance(v, str):
            return v.upper() == "TRUE"
        return bool(v)

    def to_legacy_dict(self) -> dict:
        """Convert to legacy JSON format."""
        return {
            "id": self.id,
            "label": self.label,
            "year": self.year,
            "gender": self.gender,
            "cfis": str(self.cfis).upper()
        }


class Edge(BaseModel):
    """A relationship between two people."""
    id: Optional[int] = None
    source: str
    target: str
    weight: int  # Usually 1, 2, 3, or 5
    place: str = ""
    month: str = ""  # Accepts any format (Jan, Set, Març, etc.)
    year: Optional[int] = None
    repeated: bool = False
    relationship: bool = False
    comments: Optional[str] = None

    @field_validator("year", mode="before")
    @classmethod
    def parse_year(cls, v):
        if v == "" or v is None:
            return None
        return int(v)

    @field_validator("repeated", "relationship", mode="before")
    @classmethod
    def parse_bool(cls, v):
        if v == "" or v is None:
            return False
        if isinstance(v, str):
            return v.upper() == "TRUE"
        return bool(v)

    def to_legacy_dict(self) -> dict:
        """Convert to legacy JSON format."""
        return {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "weight": self.weight,
            "place": self.place,
            "month": self.month,
            "year": self.year,
            "repeated": str(self.repeated).upper(),
            "relationship": str(self.relationship).upper(),
            "comments": self.comments
        }


class GraphData(BaseModel):
    """Complete graph data container."""
    nodes: list[Node]
    edges: list[Edge]
    unwanted: list[str] = []

    def get_node_names(self) -> set[str]:
        """Get all node labels."""
        return {n.label for n in self.nodes}

    def validate_edges(self) -> list[str]:
        """Check all edges reference valid nodes. Returns list of errors."""
        names = self.get_node_names()
        errors = []
        for e in self.edges:
            if e.source not in names:
                errors.append(f"Edge source '{e.source}' not found in nodes")
            if e.target not in names:
                errors.append(f"Edge target '{e.target}' not found in nodes")
        return errors

    def assign_ids(self) -> None:
        """Assign sequential IDs to nodes and edges."""
        for i, node in enumerate(self.nodes):
            node.id = i
        for i, edge in enumerate(self.edges):
            edge.id = i

    def apply_anonymization(self) -> "GraphData":
        """Return a copy with unwanted users anonymized."""
        mapping = {name: f"Anònim {i}" for i, name in enumerate(self.unwanted)}
        
        new_nodes = []
        for n in self.nodes:
            node_dict = n.model_dump()
            if n.label in mapping:
                node_dict["label"] = mapping[n.label]
            new_nodes.append(Node(**node_dict))

        new_edges = []
        for e in self.edges:
            edge_dict = e.model_dump()
            if e.source in mapping:
                edge_dict["source"] = mapping[e.source]
            if e.target in mapping:
                edge_dict["target"] = mapping[e.target]
            new_edges.append(Edge(**edge_dict))

        result = GraphData(nodes=new_nodes, edges=new_edges, unwanted=self.unwanted)
        result.assign_ids()
        return result

    def to_frontend_dict(self) -> dict:
        """Convert to format expected by frontend JS."""
        anonymized = self.apply_anonymization()
        return {
            "nodes": [n.to_legacy_dict() for n in anonymized.nodes],
            "edges": [e.to_legacy_dict() for e in anonymized.edges]
        }
