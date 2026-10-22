from pathlib import Path

folder = Path(input("Enter folder path: ").strip())
if not folder.is_dir():
    raise SystemExit("That path isn't a valid folder.")

categories = {
    "Images": [".png", ".jpg", ".jpeg"],
    "Notebooks": [".ipynb"],
    "PDF": [".pdf"],
    "HTML": [".html"],
    "TEXT": [".txt", ".docx"],
}

for name in categories:
    (folder / name).mkdir(exist_ok=True)

for item in folder.iterdir():
    if not item.is_file():
        continue
    for name, exts in categories.items():
        if item.suffix.lower() in exts:
            dest = folder / name / item.name
            if dest.exists():
                print(f"Skipping {item.name}, already exists in {name}")
            else:
                item.rename(dest)
            break