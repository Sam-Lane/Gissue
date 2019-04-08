import os
import requests

import pytest


from gissue.auth import Auth

@pytest.mark.order1
def test_update_token():
    if 'TRAVIS' in os.environ:
        if os.environ.get('TRAVIS_PULL_REQUEST') == 'false':
            auth = Auth()
            auth.update_token(os.environ['TOKEN'])
            home = os.path.expanduser("~")
            gissueFile = os.path.join(home, ".gissue")

            assert os.path.isfile(gissueFile)
        else:
            assert True
    else:
        pass

@pytest.mark.order2
def test_authed():
    if os.environ.get('TRAVIS_PULL_REQUEST') == 'false':
        auth = Auth()
        params = {'access_token' : auth.get_token()}

        home = os.path.expanduser("~")
        gissueFile = os.path.join(home, ".gissue")
        assert os.path.isfile(gissueFile)
        
        r = requests.get('https://api.github.com/user', params=params)
        
        assert r.status_code == 200
    else:
        assert True
