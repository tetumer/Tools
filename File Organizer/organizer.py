from pathlib import Path


folder = Path(input("Enter folder path: "))

Images = folder / "Images"
Images.mkdir(exist_ok=True)

Notebooks = folder / "Notebooks"
Notebooks.mkdir(exist_ok=True)

PDF = folder / "PDF"
PDF.mkdir(exist_ok=True)

HTML = folder / "HTML"
HTML.mkdir(exist_ok=True)

TEXT = folder / "TEXT"
TEXT.mkdir(exist_ok=True)


for item in folder.iterdir():
    if item.is_file():
        if item.suffix == ".png" or item.suffix == ".jpg" or item.suffix == ".jpeg":
            item.rename(Images / item.name)

        if item.suffix == ".ipynb":
            item.rename(Notebooks / item.name)

        if item.suffix == ".pdf":
            item.rename(PDF / item.name)

        if item.suffix == ".html":
            item.rename(HTML / item.name)

        if item.suffix == ".txt" or item.suffix == ".docx":
            item.rename(TEXT / item.name)
