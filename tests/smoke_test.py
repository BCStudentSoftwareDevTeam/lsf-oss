# Import the modules that are required for execution

import pytest
from conftest import MultipleBrowserTest 
import colorama
import urllib.request
from urllib.error import HTTPError, URLError

from app import app

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

class Test_Routes:
        verbose = False

        def test_get_routes(self, base_url, request):
            self.check_verbose_level(request)
            urls = self.get_urls("GET")
            self.url_runner(base_url, urls)

        def test_get_routes_with_params(self, base_url, request):
            self.check_verbose_level(request)
            urls = []
            self.url_runner(base_url, urls)

        def test_post_routes(self, base_url, request):
            self.check_verbose_level(request)
            urls = self.get_urls("POST")
            #self.url_runner(base_url, urls)

        def get_urls(self, method):
            """Retrieve the application routes for the given method"""

            links = []
            for rule in app.url_map.iter_rules():
                if method in rule.methods and has_no_empty_params(rule):
                    #url = url_for(rule.endpoint, **(rule.defaults or {}))
                    url = rule.rule
                    links.append((url,[]))

            return links

        def url_runner(self, base_url, urls):
            """Test a list of URLs"""

            if(self.verbose):
                print()
            for url,params in urls:
                if(self.verbose):
                    print("  {}:".format(url), end=" ")

                try:
                    assert 200 == urllib.request.urlopen('{}{}'.format(base_url, url)).getcode()
                except HTTPError as e:
                    pytest.fail("HTTPError! HTML Status Code {}".format(e.code))
                except URLError as e:
                    pytest.fail("URLError! {}".format(e.reason))
                else:
                    if(self.verbose):
                        print(colorama.Fore.GREEN + "✓" + colorama.Style.RESET_ALL)
                    pass

        def check_verbose_level(self, request):
            """Record the output level requested"""
            self.verbose = (request.config.getoption('verbose') >= 1)
