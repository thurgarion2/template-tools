"""
api provided by the package to modify template provided to the user
"""
from pathlib import Path

def edit_template(template: Path):
    """
    Take a screenshot of a sample page of the template.
    Open pinta with the screenshot, the user can modify the template,
    apply the edition to the html.
    """
    # je peux presque écrire => il me manque juste interaction avec pinta