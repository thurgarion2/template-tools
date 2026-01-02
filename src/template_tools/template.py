"""
A template is a dsl program aimed to generate a text file; 
it could simple text, html or even code.
This module is based on the model of Jinja2, it does not support different models.
"""
from abc import ABC, abstractmethod
import jinja2
from dataclasses import dataclass
from jinja2.visitor import NodeVisitor
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


######################## module spec

class TemplateSource:
    """
    Source code of a template
    """
    
    def __init__(self, name: str, content: str):
        self._name = name
        self._content = content
    
    def name(self) -> str:
        """full name with respect to the environment"""
        return self._name
    def content(self) -> str:
        """source code"""
        return self._content

class CtxVariable:
    """a template context variable"""

    def __init__(self, name: str, samples: list[str]):
        self._name = name
        self._samples = samples

    def name(self) -> str:
        """name of the variable in the context"""
        return self._name

    def samples(self) -> list[str]:
        """list of code samples where the variables is accessed"""
        return self._samples
    

class Template(ABC):
    """
    Dsl program aimed to generate a text file.
    """
    
    @abstractmethod
    def render(self, env:dict[str,str]) -> str:
        """
        render the template using the environnement
        return Value error if env do not respects the schema
        """
        raise NotImplementedError
    
    @abstractmethod
    def schema(self) -> set[CtxVariable]:
        """schema of the template"""
        raise NotImplementedError
    
    @abstractmethod
    def format(self) -> str:
        """the format of the file returned by the template"""
        raise NotImplementedError
    
    @abstractmethod
    def code(self) -> list[TemplateSource]:
        """code of the template"""
        raise NotImplementedError
    
class Environment(ABC):
    """
    Templating envrionement gather all the templates with their names.
    """
    
    @abstractmethod
    def templates(self) -> list[Template]:
        """list of all the tempplates"""
        raise NotImplementedError
    
    @abstractmethod
    def get(self, name:str) -> Template|None:
        """return template corresponding to name"""
        raise NotImplementedError
    

######################## type definition


@dataclass
class _SourceSummary:
    """
    summary of a template sources
    
    fields:
    parents -- names of all the parents it extends
    schema -- list of all the context variables
    """
    parents: set[str]
    schema: set[CtxVariable]

def _bootstrap_summary(source: str, env: jinja2.Environment) -> _SourceSummary:
    """return first iteration of sources summaries"""
    ast = env.parse(source)
    visitor = _CollectVisitor(source)
    visitor.visit(ast)
    schema = [CtxVariable(name, samples) for name, samples in visitor.variables.items()]
    

    return _SourceSummary(parents=set(visitor.extends), schema=set(schema))
    
class _CollectVisitor(NodeVisitor):
    def __init__(self, source: str):
        # we do not support correctly {% set foo = 1 %}, as we count access to foo as part of the schema

        # variable names to context
        self.variables: dict[str, list[str]] = defaultdict(lambda: [])
        self.source_lines = source.splitlines()
        self.extends: list[str] = []

    def visit_Name(self, node, *args, **kwargs):
        name = node.name
        if node.ctx == 'load':
            zero_based = node.lineno-1
            line = self.source_lines[zero_based]
            self.variables[name].append(line)
    def visit_Extends(self, node, *args, **kwargs):
        template = node.template
        if hasattr(template, "value"):
            self.extends.append(getattr(template,"value"))
        else:
            logger.warning("cannot process an extends, because it is not constant")
    

class JinjaEnvironment(Environment):
    """only supports jinja file system loader"""
    
    def __init__(self, templates: dict[str, Template]):
        self._templates = templates
    
    def templates(self) -> list[Template]:
        """list of all the tempplates"""
        return list(self._templates.values())
    
    def get(self, name: str) -> Template | None:
        """return template corresponding to name"""
        return self._templates.get(name)
    
    @classmethod
    def from_environment(cls, env: jinja2.Environment) -> 'JinjaEnvironment':
        """create jinja environement from jinja environment"""
        if env.loader is None:
            raise ValueError("a loader needs to be configured")
        
        all_templates = env.loader.list_templates()
        template_summaries: dict[str, _SourceSummary] = {}
        next_template_summaries: dict[str, _SourceSummary] = {}
        
        # compute fix point of template summaries
        for name in all_templates:
            source, _, _= env.loader.get_source(env, name)
            next_template_summaries[name] = _bootstrap_summary(source, env)
        while template_summaries!=next_template_summaries:
            template_summaries = next_template_summaries
            next_template_summaries = {}
            
            for name, summary in template_summaries.items():
                vars = set(summary.schema)
                parents = set(summary.parents)
                
                for t_name in summary.parents:
                    template = template_summaries.get(t_name)
                    if template is None:
                        logger.warning("template not found")
                        continue
                    vars = vars.union(set(template.schema))
                    parents = parents.union(set(template.parents))
                    
                next_template_summaries[name] = _SourceSummary(parents, vars)
            
        templates = {}
        for name in all_templates:
            summary = template_summaries[name]
            schema = summary.schema
            
            parents_and_name = set([name]).union(summary.parents)
            code = [TemplateSource(t_name, _source(t_name, env)) for t_name in parents_and_name]
            
            jinja_template = env.get_template(name)
            
            template_obj = JinjaHtmlTemplate(schema, code, jinja_template)
            templates[name] = template_obj
        return cls(templates)

def _source(name: str, env: jinja2.Environment):
    if env.loader is None:
        raise ValueError("do not accept env without loader")
    source, _, _ = env.loader.get_source(env, name)
    return source
        
class JinjaHtmlTemplate(Template):
    """a jinja 2 template that creates html files"""
    
    def __init__(self,
                 schema: set[CtxVariable],
                 code: list[TemplateSource],
                 template: jinja2.Template) -> None:
        self._schema = schema
        self._code = code
        self._template = template

    def render(self, env: dict[str, str]) -> str:
        """
        render the template using the environnement
        return Value error if env do not respects the schema
        """
        required_vars = {var.name() for var in self._schema}
        if not required_vars.issubset(env.keys()):
            raise ValueError(f"Missing variables: {required_vars - set(env.keys())}")
        return self._template.render(env)

    def schema(self) -> set[CtxVariable]:
        """schema of the template"""
        return self._schema

    def code(self) -> list[TemplateSource]:
        """code of the template"""
        return self._code

    def format(self) -> str:
        return "html"