# Changelog

## [2.3.2] - 2024-12-20

### Added
- **Favicon & Meta Tags**: Rounded logo as favicon with Open Graph/Twitter meta tags for social sharing
- **Logout Button**: "Sortir" button in sidebar to clear session and return to login
- **Session Security**: 
  - Password only stored in sessionStorage on successful login
  - Direct access to graph.html without login redirects to login page
  - Decryption failure clears session and redirects to login

### Improved
- **Login Flow**: Password now stored only when login button pressed (not on keystroke)
- **Url Parameters**: Removed referrer-based auth that broke on tunnels

### Fixed
- **Session Timing**: Added small delay for sessionStorage sync after login redirect

### Removed
- Debug console.log statements from `network-creation.js`
- Unused `referrer.js` include from `graph.html`

---

## [2.3.1] - 2024-12-20

### Fixed
- **HTML Compliance**: Added missing `<!DOCTYPE html>` declaration to `graph.html`
- **Accessibility**: Changed `lang` attribute from "en" to "ca" (Catalan)
- **JavaScript Bug**: Fixed undefined `err` variable in `login/js/main.js` catch block
- **Duplicate Declarations**: Removed duplicate `filterPanel`/`filterToggle` variables in `graph.html`
- **Password Handling**: Changed from `onblur` to `oninput` for more reliable password capture

### Improved
- **SEO**: Added meta description tag to `graph.html`
- **CSS Cleanup**: Removed unused `.input1` and `.my-legend` legacy styles (~80 lines)
- **Year Range**: Extended year validation from 2030 to 2100 in `models.py` and widgets
- **Colors**: Added year colors for 2025-2030 in `global-variables.js`

---

## [2.3.0] - 2024-12-20

### Added
- **Admin Notebook** (`Admin-Notebook.ipynb`) for advanced graph management:
  - JSON sync: Export/Import data as plain JSON for external editing
  - Delete decrypted JSON prompt after import (security)
  - Edge management: Search, Modify, Delete edges
  - User deletion: Complete node removal with all connected edges
- **Auto-load password** from `.env` file (optional convenience)
- **Security**: `_config.yml` to exclude sensitive files from GitHub Pages

### Improved
- Role separation: `Graph-updater.ipynb` is now read-only for edges (add/search only)
- Fixed duplicate button callback issue on module reload
- README updated with security documentation and file role explanations

---

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
