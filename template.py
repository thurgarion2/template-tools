"""
contain code related to the interaction with the jinja template
"""
from pathlib import Path
import pydantic
from dataclasses import dataclass

class Html:
    
    def __init__(self, html: str) -> None:
        """
        the constructor should only be used in template.py
        """
        self._html = html
        
    def text(self) -> str:
        return self._html
    

class JinjaContext:
    """
    all the context of a jinja template
    """
    
    def __init__(self, root: Path) -> None:
        """
        :param root: the path to the root jinja template
        """
        self._root = root
        
    def templates(self) -> dict[str,Path]:
        """
        Provides the list of templates involved in the rendering.
        If the root template is self contained, then only the root.
        If the root extend another template, then both of them.
        
        :return: mapping from template name to Path
        """
        # TODO implement the method using what???
        
    def schema(self) -> pydantic.BaseModel:
        """
        The json schema of the template context.
        
        :return: json schema
        """
        # TODO implement the method
        # jsonschema
        
        # le plan c'est une routine de génération de pydantic model dans un fichier spécifique
        # je vais utiliser exec avec un context spécifique
        # le modèle doit être un modèle pydantic valide et doit être le schema du template => instancier
        
    def render(self, context: dict) -> Html:
        """
        :param context: context of the template, must respect schema
        :return: rendered template
        raises ValueError: if there is a problem with the rendering
        """
        # TODO implement the method

@dataclass
class Error:
    message: str


def _eval_pydantic_model(code: str) -> pydantic.BaseModel|Error:
    """
    evaluate code creating a pydantic model, return the model or an error message
    """
    