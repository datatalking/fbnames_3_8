import nbformat
from nbconvert import PythonExporter

# Open the notebook file
with open("2021-billionaires-eda.ipynb", "r", encoding="utf-8") as f:
    notebook_content = f.read()

# Parse the notebook content
notebook_node = nbformat.reads(notebook_content, as_version=4)

# Export as Python script
exporter = PythonExporter()
script, _ = exporter.from_notebook_node(notebook_node)

# Write to .py file
with open("2021-billionaires-eda.py", "w", encoding="utf-8") as f:
    f.write(script)
