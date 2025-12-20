# Changelog

## [2.2.0] - 2024-12-20

### Improved
- **UI Modernization**: Complete layout overhaul
  - Overlay sidebar on all screen sizes
  - Mobile: Hidden header, floating menu button, full-screen graph
  - Pan & Zoom support for graph exploration
- **Dynamic Filters**:
  - Replaced hardcoded year buttons with `bootstrap-select` dropdowns
  - Auto-populated years from graph data (no manual HTML editing needed)
  - Display birth year in node selector
- **Layout & Usability**:
  - Collapsible filter panel (translucent square mode)
  - Optimized sidebar layout and z-index layering (3000+) to fix overlaps
  - Autocomplete results now dropdown correctly using absolute positioning
  - Flexbox-based search bar for pixel-perfect vertical alignment

### Fixed
- Instagram link positioning in sidebar
- Search button visibility and size consistency issues
- Mobile touch targets and font sizing

---

## [2.1.0] - 2024-12-20

### Improved
- **Graph-updater notebook** completely rewritten with better documentation
- Split edge UI: separate sections for "Add" and "Search/Modify/Delete"
- Node UI: vertical layout with dynamic birth year helper
- Edge defaults: year and month auto-set to current date
- Modify edge: can now edit all fields (year, month, place, comments)

### Removed
- `data_generator.py` - functionality moved to `storage.py`

---

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
