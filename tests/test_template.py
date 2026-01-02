import pytest
import jinja2
from pathlib import Path
from template_tools.template import JinjaEnvironment

@pytest.fixture
def jinja_env():
    loader = jinja2.FileSystemLoader(Path(__file__).parent / "data" / "template" / "proj1")
    env = jinja2.Environment(loader=loader)
    return JinjaEnvironment.from_environment(env)

def test_single_template_render(snapshot, jinja_env):
    template = jinja_env.get("single.html")
    env = {
        "title": "Test Page",
        "name": "Alice",
        "age": 25,
        "items": ["apple", "banana", "cherry"],
        "greeting": "Hello",
        "item": "dummy"
    }
    result = template.render(env)
    snapshot.assert_match(result, "single_render")

def test_single_template_schema(snapshot, jinja_env):
    template = jinja_env.get("single.html")
    schema = template.schema()
    schema_data = [{"name": var.name(), "samples": var.samples()} for var in schema]
    schema_data.sort(key=lambda d: d["name"])
    snapshot.assert_match(str(schema_data), "single_schema")

def test_single_template_code(jinja_env):
    template = jinja_env.get("single.html")
    names = [code.name() for code in template.code()]
    assert names ==  ["single.html"]

def test_single_template_format(jinja_env):
    template = jinja_env.get("single.html")
    assert template.format() == "html"

def test_extends_template_render(snapshot, jinja_env):
    template = jinja_env.get("extends.html")
    env = {
        "page_title": "Extended Page",
        "user": "Bob",
        "message": "Welcome to the site",
        "show_list": True,
        "list_items": ["item1", "item2"],
        "year": 2023,
        "header_msg": "Welcome",
        "item": "dummy"
    }
    result = template.render(env)
    snapshot.assert_match(result, "extends_render")

def test_extends_template_schema(snapshot, jinja_env):
    template = jinja_env.get("extends.html")
    schema = template.schema()
    schema_data = [{"name": var.name(), "samples": var.samples()} for var in schema]
    schema_data.sort(key=lambda d: d["name"])
    snapshot.assert_match(str(schema_data), "extends_schema")

def test_extends_template_code(jinja_env):
    template = jinja_env.get("extends.html")
    names = [code.name() for code in template.code()]
    names.sort()
    assert names ==  ['extends.html', 'parent.html']

def test_extends_template_format(jinja_env):
    template = jinja_env.get("extends.html")
    assert template.format() == "html"

def test_extends2times_template_render(snapshot, jinja_env):
    template = jinja_env.get("extends2times.html")
    env = {
        "page_title": "Double Extended Page",
        "subtitle": "Sub Title",
        "content": "Main content here",
        "show_extra": True,
        "extra": "Extra info",
        "year": 2023
    }
    result = template.render(env)
    snapshot.assert_match(result, "extends2times_render")

def test_extends2times_template_schema(snapshot, jinja_env):
    template = jinja_env.get("extends2times.html")
    schema = template.schema()
    schema_data = [{"name": var.name(), "samples": var.samples()} for var in schema]
    schema_data.sort(key=lambda d: d["name"])
    snapshot.assert_match(str(schema_data), "extends2times_schema")

def test_extends2times_template_code(jinja_env):
    template = jinja_env.get("extends2times.html")
    names = [code.name() for code in template.code()]
    names.sort()
    assert names == ["extends2times.html", "parent.html", "parent1time.html"]

def test_extends2times_template_format(jinja_env):
    template = jinja_env.get("extends2times.html")
    assert template.format() == "html"
