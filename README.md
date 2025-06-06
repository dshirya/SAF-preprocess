# SAF-preprocess


## How to run 
1. Download the code or clone the repository to your computer:

```bash
cd {directory where you want to download the code}
```
```bash 
git clone https://github.com/dshirya/SAF-preprocess.git
``` 
2. Open the terminal and go to the folder with the program
```bash 
cd SAF-preprocess
```
3. Create conda environment and install the packages
```bash
conda create -n {env name} python=3.13
```

```bash
conda ativate {env name} 
```

```bash
pip install -r requirements.txt
```
4. Put folders with .cif files to the same directory with `main.py`
5. Run the code
```bash
python main.py 
```
## Features

- Scans subdirectories for `.cif` files.
- Interactive CLI using `click` to select folders and choose sort order (ascending/descending by Mendeleev number).
- Extracts chemical formulas from CIF files via `cifkit`.
- Sorts elements in each formula by Mendeleev number.
- Supports only binary, ternary, and quaternary compounds.
- Creates a `labels/` folder in each processed directory:
  - `sorted_compounds.xlsx` with separate sheets per compound type (`AB`, `RMX`, `ABCD`). - for CAF
  - `element_labels.txt` listing unique element labels for each position (A, B, R, M, X, C, D). - for SAF
- Uses logging for error handling and progress reporting.
