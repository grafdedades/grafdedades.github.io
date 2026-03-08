import json
from pathlib import Path

# Paths to the json file
DATA_FILE = Path("d:/grafdedades.github.io/data/decrypted_graph.json")

def process():
    if not DATA_FILE.exists():
        print(f"Error: {DATA_FILE} not found.")
        return

    # Month mapping from strings to integers
    month_map = {
        'Jan': 1, 'Gener': 1,
        'Feb': 2, 'Febrer': 2,
        'Mar': 3, 'Març': 3,
        'Apr': 4, 'Abril': 4,
        'May': 5, 'Maig': 5,
        'Jun': 6, 'Juny': 6,
        'Jul': 7, 'Juliol': 7,
        'Aug': 8, 'Agost': 8,
        'Sep': 9, 'Setembre': 9, 'Set': 9,
        'Oct': 10, 'Octubre': 10,
        'Nov': 11, 'Novembre': 11,
        'Dec': 12, 'Desembre': 12,
        'Desconegut': None, '': None
    }
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    edges_modified = 0

    for edge in data.get("edges", []):
        m = edge.get("month")
        
        # Already an integer
        if isinstance(m, int):
            continue
            
        # None value
        if m is None:
            continue
            
        # String processing
        if isinstance(m, str):
            m_str = m.strip()
            
            # Already a number as string
            if m_str.isdigit():
                edge["month"] = int(m_str)
                edges_modified += 1
                continue
            
            # Empty string
            if m_str == "":
                edge["month"] = None
                edges_modified += 1
                continue
                
            # Dictionary lookup
            if m_str in month_map:
                edge["month"] = month_map[m_str]
                edges_modified += 1
                continue
                
            print(f"Warning: Unknown month format '{m_str}' in edge ID {edge.get('id', 'unknown')}")

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully migrated {edges_modified} edges in month field to integers.")

if __name__ == '__main__':
    process()
