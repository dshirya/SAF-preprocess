import os
from typing import List

def contains_cif_files(directory: str) -> bool:
    return any(file.endswith(".cif") for file in os.listdir(directory))

def get_cif_dir_names(script_path: str) -> List[str]:
    return [
        os.path.basename(d)
        for d in os.listdir(script_path)
        if os.path.isdir(os.path.join(script_path, d))
        and not d.startswith("tests")
        and contains_cif_files(os.path.join(script_path, d))
    ]

def get_file_paths(folder: str) -> List[str]:
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".cif") and os.path.isfile(os.path.join(folder, f))
    ]

