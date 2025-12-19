# Changelog

## [2.0.0] - 2024-12-19

### Changed
- **Backend rewritten** with modular Python architecture
- Encryption now uses PBKDF2 key derivation (100k iterations)
- Single source of truth: `graph_data.enc` replaces 3 separate files
- Added Pydantic validation for data integrity

### Added
- `tools/models.py` - Data models with validation
- `tools/crypto.py` - Secure encryption module
- `tools/storage.py` - File I/O with auto-backup
- `requirements.txt` - Python dependencies
- `.gitignore` - Prevent committing sensitive files

### Removed
- Legacy `encrypted_nodes.txt`, `encrypted_edges.txt`, `encrypted_unwanted.txt`
- Dependency on Node.js for backend encryption

---

## [1.0.0] - 2021

- Initial release with D3.js visualization
- Node.js + Python hybrid encryption
- Jupyter notebook for data updates
