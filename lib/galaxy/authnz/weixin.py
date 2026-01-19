import re
from social_core.backends.weixin import WeixinOAuth2

class WeixinAuth2(WeixinOAuth2):
    name = 'weixin'

    def user_data(self, access_token, *args, **kwargs):
        data = super().user_data(access_token, *args, **kwargs)
        if not data.get('id_token'):
            data['id_token'] = "dummy"
        return data

    def get_user_id(self, details, response):
        uid = response.get('unionid') or response.get('openid')
        return uid.lower()

    def get_user_details(self, response):
        data = super().get_user_details(response)
        uid = self.get_user_id({}, response)
        if not uid:
            return data
        username = re.sub(r'[^a-z0-9_]', '_', uid.lower())
        data['username'] = username
        if not data.get('email') and username:
            data['email'] = f"{username}@dummy.com"
        return data
