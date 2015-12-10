# -*- coding: utf-8 -*-
import re
import json

from socialoauth.sites.base import OAuth2
from socialoauth.exception import SocialAPIError


QQ_OPENID_PATTERN = re.compile('\{.+\}')

class QQApp(OAuth2):
    AUTHORIZE_URL = 'https://graph.qq.com/oauth2.0/authorize'
    ACCESS_TOKEN_URL = 'https://graph.qq.com/oauth2.0/token'

    OPENID_URL = 'https://graph.qq.com/oauth2.0/me'


    @property
    def authorize_url(self):
        url = super(QQ, self).authorize_url
        return '%s&state=socialoauth' % url


    def get_access_token(self, code):
        super(QQ, self).get_access_token(code, method='GET', parse=False)


    def build_api_url(self, url):
        return url

    def build_api_data(self, **kwargs):
        data = {
            'access_token': self.access_token,
            'oauth_consumer_key': self.CLIENT_ID,
            'openid': self.uid
        }
        data.update(kwargs)
        return data

    def parse_token_response(self, res):
        self.uid = res['userid']
        self.access_token = res['access_token']
        self.expires_in = None
        self.refresh_token = None

        _url = 'https://graph.qq.com/user/get_user_info'
        res = self.api_call_get(_url)
        if res['ret'] != 0:
            raise SocialAPIError(self.site_name, _url, res)

        self.name = res['nickname']
        self.avatar = res['figureurl_qq_1']
        self.avatar_large = res['figureurl_qq_2']
        self.gender = res['gender']
