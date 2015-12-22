# -*- coding: utf-8 -*-

from socialoauth.sites.base import OAuth2

class FacebookApp(OAuth2):
    GRAPH_URL        = 'https://graph.facebook.com'
    AUTHORIZE_URL    = 'https://www.facebook.com/dialog/oauth'
    ACCESS_TOKEN_URL = '{0}/oauth/access_token'.format(GRAPH_URL)

    def build_api_url(self, url):
        return url

    def build_api_data(self, **kwargs):
        data = {
            'access_token': self.access_token
        }
        data.update(kwargs)
        return data

    def parse_token_response(self, res):
        self.access_token = res['accessToken']
        self.expires_in = int(res['expiresIn'])
        self.uid = res['userId']
        self.refresh_token = None

        res = self.api_call_get(self.GRAPH_URL+'/me?fields=name,gender,picture', {
            'access_token': self.access_token
        })
        print res

        self.name = res['name']
        self.avatar = res['picture']['data']['url']
        self.avatar_large = self.avatar
        self.gender = res['gender'] == u"male" and "M" or "F"
