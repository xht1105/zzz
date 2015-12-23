# -*- coding: utf-8 -*-

from socialoauth.sites.base import OAuth2

class Facebook(OAuth2):
    GRAPH_URL        = 'https://graph.facebook.com'
    AUTHORIZE_URL    = 'https://www.facebook.com/dialog/oauth'
    ACCESS_TOKEN_URL = '{0}/oauth/access_token'.format(GRAPH_URL)

    @property
    def authorize_url(self):
        url = super(Facebook, self).authorize_url
        return '%s&scope=email,public_profile,user_friends&state=socialoauth' % url

    def build_api_url(self, url):
        return url

    def build_api_data(self, **kwargs):
        data = {
            'access_token': self.access_token,
            'fields': 'name,gender,picture.type(large)',
        }
        data.update(kwargs)
        return data

    def parse_token_response(self, res):
        res = res.split('&')
        res = [_r.split('=') for _r in res]
        res = dict(res)

        self.access_token = res['access_token']
        self.expires_in = int(res['expires'])
        self.uid = res['userID']
        self.refresh_token = None

        res = self.api_call_get(self.GRAPH_URL+'/me')

        self.name = res['name']
        self.avatar = res['picture']['data']['url']
        self.avatar_large = self.avatar
        self.gender = res['gender'] == u"male" and "M" or "F"

    def get_access_token(self, code):
        super(Facebook, self).get_access_token(code, method='GET', parse=False)
