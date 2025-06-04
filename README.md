# SAF-preprocess

**Features**:
- Scans subdirectories for `.cif` files (excluding `tests*` folders).
- Interactive CLI using `click` to select folders and choose sort order (ascending/descending by Mendeleev number).
- Extracts chemical formulas from CIF files via `cifkit`.
- Sorts elements in each formula by Mendeleev number.
- Supports only binary, ternary, and quaternary compounds.
- Creates a `labels/` folder in each processed directory:
  - `sorted_compounds.xlsx` with separate sheets per compound type (`AB`, `RMX`, `ABCD`).
  - `element_labels.txt` listing unique element labels for each position (A, B, R, M, X, C, D).
- Uses logging for error handling and progress reporting.

**Usage**:
```bash
python main.py