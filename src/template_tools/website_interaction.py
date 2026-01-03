"""
Support methods to setup a website and interact with it.
Module support only creating 1 website at a time and opening 1 page at a time.
"""
from abc import ABC, abstractmethod
from pathlib import Path 
from playwright.sync_api import Page
from contextlib import contextmanager



######################## module spec


class Website(ABC):
    """
    Collection of resources: html file, css sheet, ..., served on a web server.
    Only 1 website can be open at a time.
    """
    
    @abstractmethod
    def open_page(self, path: Path) -> Page:
        """
        open a page of the site, return a Value error if the page is not found.
        """
        raise NotImplementedError
        

######################## implementation

# create an http sever in a different thread

class SimpleWebsite(Website):
    """simple in memory website, use chrome"""
    
    @contextmanager
    @classmethod
    def create(cls, resources: dict[Path,str]):
        #TODO implement
        pass
        
    
    def __init__(self, resources: dict[Path,str]) -> None:
        self._resources = resources