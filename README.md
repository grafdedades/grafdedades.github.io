# Graf de Dades

Interactive social network visualization with D3.js and encrypted data storage.

[![GitHub Pages](https://img.shields.io/badge/Hosted%20on-GitHub%20Pages-blue)](https://grafdedades.github.io)
[![Instagram](https://img.shields.io/badge/Instagram-@data.graf-E4405F)](https://instagram.com/data.graf)

## Quick Start

### Viewing the Graph

```bash
python -m http.server 3000
# Open http://localhost:3000
```

### Updating Data

```bash
pip install -r requirements.txt
jupyter notebook Graph-updater.ipynb
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
│   ├── graph_data.enc      # Source of truth
│   └── encrypted_data.txt  # Frontend data
├── tools/
│   ├── models.py           # Data models
│   ├── crypto.py           # Encryption
│   └── storage.py          # File I/O
└── js/                     # D3 visualization
```

---

## Data Protection

All data is encrypted at rest using Fernet symmetric encryption:
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
| Year filters | Filter by cohort |

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

## Yearly Maintenance

1. `js/global-variables.js` — Add color for new year
2. `graph.html` — Add year selector buttons
3. `js/network-creation.js` — Add filter handlers

---

## Authors

- **Pau Matas** (original)
- **Álvaro Domingo** (maintainer)
- grafdedades@gmail.com
