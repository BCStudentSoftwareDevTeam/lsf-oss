# Import the modules that are required for execution

import pytest
import colorama
import urllib.request
from urllib.error import HTTPError, URLError
from time import sleep
import socket 
import http.client

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

            # Commented out URLs currently have an error
            urls = [
                ("/laborHistory/modal/printPdf/2", []),
                ("/admin/emailTemplates/getPurpose/student", []),
                ("/admin/emailTemplates/getPurpose/students", []),
                ("/admin/emailTemplates/getPurpose/supervisor", []),
                ("/admin/emailTemplates/getPurpose/breakPrimary", []),
                ("/admin/emailTemplates/getEmail/Labor%20Status%20Form%20Submitted%20For%20Student", []),
                ("/laborstatusform/getcompliance/1", []),
                ("/laborstatusform/getPositions/1", []),
                # ("/laborstatusform/getstudents/<termCode>/<student>/<isOneLSF>", []),
                ("/laborstatusform/getstudents/202000/B00841417", []),
                ("/laborstatusform/getDate/202000", []),
                ("/laborHistory/modal/2", []),
                ("/admin/pendingForms/<formType>", []),
                ("/admin/getNotes/2", []),
                ("/main/department/<departmentSelected>", []),
                #("/studentOverloadApp/1", []),
                # ("/laborReleaseForm/<laborStatusKey>", []),
                ("/laborstatusform/2", []),
                ("/laborHistory/<id>", []),
                # ("/adjustLSF/<laborStatusKey>", []),
                # ("/modifyLSF/<laborStatusKey>", []),
            ]
            self.url_runner(base_url, urls)

        def test_post_routes(self, base_url, request):
            self.check_verbose_level(request)
            urls = [
                # ("/laborHistory/modal/updatestatus", []),
                # ("/admin/emailTemplates/postEmail/", []),
                # ("/studentOverloadApp/update", []),
                # ("/laborstatusform/userInsert", []),
                # ("/adminManagement/userInsert", []),
                # ("/termManagement/manageStatus", []),
                # ("/termManagement/setDate", []),
                # ("/laborHistory/download", []),
                # ("/admin/complianceStatus", []),
                # ("/admin/termManagement", []),
                # ("/admin/checkedForms", []),
                # ("/adjustLSF/submitModifiedForm/<laborStatusKey>", []),
                # ("/modifyLSF/updateLSF/<laborStatusKey>", []),
                # ("/admin/updateStatus/<raw_status>", []),
                # ("/admin/notesInsert/<formId>", []),
                # ("/laborReleaseForm/<laborStatusKey>", []),
            ]
            self.url_runner(base_url, urls)

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
                sleep(.1) # Without this sleep we end up with Remote Disconnect exceptions
                if(self.verbose):
                    print("  {}:".format(url), end=" ")

                try:
                    assert 200 == urllib.request.urlopen('{}{}'.format(base_url, url)).getcode()
                except HTTPError as e:
                    pytest.fail("HTTPError! HTML Status Code {}".format(e.code))
                except URLError as e:
                    pytest.fail("URLError! {}".format(e.reason))
                except socket.timeout as e:
                    pytest.fail("Timeout!")
                except http.client.HTTPException as e:
                    pytest.fail("Remote Disconnected!")
                else:
                    if(self.verbose):
                        print(colorama.Fore.GREEN + "✓" + colorama.Style.RESET_ALL)
                    pass

        def check_verbose_level(self, request):
            """Record the output level requested"""
            self.verbose = (request.config.getoption('verbose') >= 1)
