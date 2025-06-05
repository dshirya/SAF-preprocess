#!filepath: main.py
import os
import re
import logging
import click
import pandas as pd
from collections import defaultdict
from typing import Dict, List, Tuple
from cifkit import Cif
from utils.mendeleev_number import get_mendeleev_numbers
import utils.folder as folder
import utils.prompt as prompt

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

mendeleev_numbers = get_mendeleev_numbers()

@click.command()
def main() -> None:
    script_path = os.path.dirname(os.path.abspath(__file__))
    dir_names_with_cif = folder.get_cif_dir_names(script_path)
    selected_dirs = prompt.get_user_input_folder_processing(dir_names_with_cif, ".cif")

    for idx, (_, dir_path) in enumerate(selected_dirs.items(), start=1):
        prompt.prompt_folder_progress(idx, dir_path, len(selected_dirs))
        sort_direction = click.prompt(
            f"Sort formulas in '{dir_path}' by mendeleev number (ascending/descending)?", 
            type=click.Choice(["asc", "desc"]),
            default="asc"
        )
        compound_map, element_labels = process_folder(dir_path, sort_direction)
        save_outputs(dir_path, compound_map, element_labels)

def process_folder(dir_path: str, sort: str) -> Tuple[Dict[str, List[Dict[str, str]]], Dict[str, set]]:
    compound_map: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    element_labels: Dict[str, set] = defaultdict(set)
    for file_path in folder.get_file_paths(dir_path):
        try:
            cif = Cif(file_path)
            parsed = parse_formula_elements(cif.formula)
            symbols = [sym for sym, _ in parsed]
            if 2 <= len(symbols) <= 4:
                sorted_tuples = sorted(
                    parsed,
                    key=lambda pair: mendeleev_numbers.get(pair[0], float("inf")),
                    reverse=(sort == "desc"),
                )
                sorted_formula = "".join([f"{sym}{cnt}" for sym, cnt in sorted_tuples])
                label_list = get_label_key(len(sorted_tuples))
                key_str = "".join(label_list)
                compound_map[key_str].append({
                    "Filename": os.path.basename(file_path),
                    "Formula": sorted_formula,
                    "Structure": cif.structure,
                })
                for i, (sym, _) in enumerate(sorted_tuples):
                    element_labels[f"{label_list[i]}_labels"].add(sym)
        except Exception as e:
            logging.warning(f"Failed to parse {file_path}: {e}")
    return compound_map, element_labels

def parse_formula_elements(formula: str) -> List[Tuple[str, str]]:
    return re.findall(r"([A-Z][a-z]*)(\d*\.?\d*)", formula)

def get_label_key(length: int) -> List[str]:
    return {
        2: ["A", "B"],
        3: ["R", "M", "X"],
        4: ["A", "B", "C", "D"],
    }[length]

def save_outputs(dir_path: str, 
                 compound_map: Dict[str, List[Dict[str, str]]], 
                 element_labels: Dict[str, set]) -> None:
    labels_folder = os.path.join(dir_path, "labels")
    os.makedirs(labels_folder, exist_ok=True)
    excel_path = os.path.join(labels_folder, "sorted_compounds.xlsx")
    txt_path = os.path.join(labels_folder, "element_labels.txt")
    with pd.ExcelWriter(excel_path) as writer:
        for key_str, compounds in compound_map.items():
            df = pd.DataFrame(compounds)
            df.to_excel(writer, sheet_name=key_str, index=False)
    with open(txt_path, "w") as f:
        for label, elements in element_labels.items():
            f.write(f"{label} = [\n")
            for el in sorted(elements):
                f.write(f"    \"{el}\",\n")
            f.write("]\n\n")

if __name__ == "__main__":
    main()