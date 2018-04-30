from __future__ import (absolute_import, division, print_function, unicode_literals)
from future import standard_library  # noqa
from builtins import *  # noqa

import requests
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


class LoginError(Exception):
    pass


class pyBNS(object):
    # Declare properties
    # Username and password are pulled from arguments given in instance.
    def __init__(self, *args, **kwargs):
        # go through keyword arguments
        for key, value in list(kwargs.items()):
            # if the keys are username and password, set self attributes
            if key in ['username', 'password']:
                setattr(self, key, value)
        # base url
        self.api_url = 'https://api.bloomberg.com/{0}'
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'authorization': 'Basic YkFSeWpFbGxWTGZHSmlYd2FlOFJpMHUzZVFRYTpKOVhDYmhiMG9zMFBPOGNEYUIwSlY5Z1JDMW9h'
        }

    def post(self, url, payload):
        url = self.api_url.format(url)
        # try posting the complete url, credentials and headers
        r = requests.post(url=url, data=payload, headers=self.headers)
        # raise an exception if it's not 200
        r.raise_for_status()
        return r

    def get(self, url):
        # headers for the get request
        get_header = {
            'content-type': 'application/json',
            'authorization': 'Bearer {0}'.format(self.access_token)
        }
        # set up the url
        url = self.api_url.format(url)
        # try requesting a story
        r = requests.get(url=url, headers=get_header)
        # raise exception if it's not 200
        r.raise_for_status()
        # return the response
        return r

    def connect(self):
        # If there's not a username and password, raise an exception
        try:
            # quote username and password to get the special url encoding
            username = quote(self.username)
            password = quote(self.password)
        except AttributeError:
            msg = 'pyBNS instance requires a username and password'
            raise LoginError(msg)

        login_data = 'username={0}&password={1}&remember=false&grant_type=password'.format(username, password)
        # pass through url ending and payload
        response = self.post('syndication/token', login_data)
        # save access token for later use
        self.access_token = str(response.json()['access_token'])

    def get_story(self, story_id):
        # request the json from this url with the story id at the end
        r = self.get('syndication/stage/portal/adapter/v1/api/v1/articles/{0}'.format(story_id))
        return r.json()

    def disconnect(self):
        try:
            payload = 'token={0}'.format(self.access_token)
            # post token to api
            self.post('syndication/revoke', payload)
        except AttributeError as e:
            print(e)