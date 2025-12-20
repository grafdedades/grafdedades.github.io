# Graf de Dades

Interactive social network visualization with D3.js and encrypted data storage.

[![GitHub Pages](https://img.shields.io/badge/Hosted%20on-GitHub%20Pages-blue)](https://grafdedades.github.io)
[![Instagram](https://img.shields.io/badge/Instagram-@data.graf-E4405F)](https://instagram.com/data.graf)

---

## Yearly Maintenance

1. **Update Colors**: Add a new color code for the new year in `js/global-variables.js` (`colors` array).
2. **Update Data**: Use the notebook to add new nodes/edges.

That's it! The year selectors and filters update automatically.

---

## Quick Start

### Initial Setup (Optional)
To avoid entering the password every time:
```bash
cp .env.example .env
# Edit .env and set your PASSWORD
```

### Updating Data
```bash
pip install -r requirements.txt
jupyter notebook Graph-updater.ipynb
```

### Viewing the Graph

```bash
python -m http.server 3000
# Open http://localhost:3000
```

---

## Architecture

| Component | Technology |
|-----------|------------|
| Visualization | D3.js v3.5.5 |
| Frontend | HTML5, Bootstrap 4.5 |
| Encryption | Fernet (AES-128-CBC + HMAC) |
| Backend | Python 3, Pydantic |

### Project Structure

```
grafdedades.github.io/
├── index.html              # Login page
├── graph.html              # Visualization
├── data/
│   ├── graph_data.enc      # ADMIN ONLY: Source of truth (Full data)
│   └── encrypted_data.txt  # PUBLIC: Frontend data (Anonymized)
├── tools/
│   ├── models.py           # Data models
│   ├── crypto.py           # Encryption
│   └── storage.py          # File I/O
└── js/                     # D3 visualization
```

---

## Data Protection & Security

All data is encrypted at rest using Fernet symmetric encryption.

### File Roles
- **`data/graph_data.enc`**: The **Source of Truth**. It contains all data including the real names of people marked as "unwanted". This file is used only by the Python Admin tools and is **NOT** served by the website.
- **`data/encrypted_data.txt`**: The **Public File**. This is generated automatically when you save. It contains "Anònim X" placeholders instead of real names for unwanted people. This is the only file the website (browser) downloads.

### Encryption Details
- Decryption happens client-side in the browser
- Password never transmitted over network
- PBKDF2 key derivation (100k iterations)

---

## Graph Features

| Feature | Description |
|---------|-------------|
| Click node | Highlight connections |
| Click edge | Show details |
| Search | Find a person |
| Year filters | Multi-select by cohort (Dynamic) |
| Pan & Zoom | Explore graph freely |

---

## API Reference

```python
from tools import load_graph_data, save_graph_data, Node, Edge

# Load
data = load_graph_data(password)

# Add node
data.nodes.append(Node(label="Name", year=2024, gender="F", cfis=False))

# Save (auto-backup)
save_graph_data(data, password)
```

---

## Data Schema

When decrypted, the graph data has this structure:

### Node (Person)
```json
{
  "id": 0,
  "label": "Nom Cognom",
  "year": 2023,
  "gender": "F",
  "cfis": false
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Auto-assigned sequential ID |
| `label` | string | Full name (unique) |
| `year` | int | University entry year (2017-2030) |
| `gender` | "F" / "M" / "-" | Gender |
| `cfis` | bool | Is CFIS student |

### Edge (Relationship)
```json
{
  "id": 0,
  "source": "Persona 1",
  "target": "Persona 2",
  "weight": 3,
  "place": "Barcelona",
  "month": "Sep",
  "year": 2023,
  "repeated": false,
  "relationship": true,
  "comments": null
}
```

| Field | Type | Description |
|-------|------|-------------|
| `weight` | 1/2/3/5 | Lio=1, Manual=2, Oral=3, Complert=5 |
| `place` | string | Location |
| `month` | string | Month (Jan, Feb, ..., Dec, or empty) |
| `year` | int | Year of event |
| `repeated` | bool | If they repeated |
| `relationship` | bool | If they have/had a relationship |

### Unwanted (Anonymized)
```json
{
  "unwanted": ["Persona 1", "Persona 2"]
}
```

People in this list appear as "Anònim X" in the public graph.

---

## Authors

- **Pau Matas** (original)
- **Álvaro Domingo** (maintainer)
- grafdedades@gmail.com

