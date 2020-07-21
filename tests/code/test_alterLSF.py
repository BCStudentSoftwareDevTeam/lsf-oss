import pytest
from app.controllers.main_routes.alterLSF import submitAlteredLSF
# from correct.package import _BASE_URL
from requests import HTTPError
import requests
import requests_mock

@pytest.mark.integration
def test_submitAlteredLSF(requests_mock):
    laborStatusKey = 2
    test = requests_mock.get(f'/alterLSF/submitAlteredLSF/{laborStatusKey}', json={'supervisor':{'oldValue':'1', 'newValue':'2', 'date': '07/21/2020'}})
    print('test', test)
    response = submitAlteredLSF(2)
    print('resp', response)
