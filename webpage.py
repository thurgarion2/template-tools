"""
handle interaction with web pages
"""
from PIL import Image

# the module use http sever and playwright in a different thread
# to make possible the interaction

class Webserver:
    """
    control the http server in a thread
    """
    
    def serve_files(self, files: dict[str, str]):
        pass
    
class Playwright:
    """
    control playwright
    """
    
    def screenshot(self, page: str):
        pass

class WebPageService:
    """
    Service use to create a webpage and interact with it.
    """
    
    # we need to support resources with the server
    def screenshot(self, html: str) -> Image:
        """
        given an html return a screenshot of the page
        """
        pass
    
    
        