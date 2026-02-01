import re
import string
import random
from social_core.backends.weixin import WeixinOAuth2

class WeixinOIDC(WeixinOAuth2):
    """Weixin OIDC backend"""

    name = 'weixin'
    ID_KEY = "unionid"

    def user_data(self, access_token, *args, **kwargs):
        data = super().user_data(access_token, *args, **kwargs)
        if not data.get('id_token'):
            data['id_token'] = "dummy"
        return data

    def get_user_details(self, response):
        # New user: random username, email, and password 
        # 随机用户名邮箱不可行，新版本认证流程，会让用户先确认创建新账户，在确认页面，用户确认之后
        # 会创建用户，这时候认证流程已经中断了。只通过用户名和邮箱创建了新账户
        # 但还没有跟社交账户关联，关联要靠用户再次扫码时，通过邮箱自动绑定。如果邮箱是随机的，那就永远也不可能自动绑定。
        # 因此邮箱必须要用固定值。当然，一旦绑定，用户名和邮箱都可以改，以后登录，只看社交账号了。因为是关联到用户id的，其他信息都可以改。

        # 邮箱必须跟微信id关联上，用户名呢，这个可以考虑下。要看用户名有没有用于查询数据库，如果有，也必须跟微信id关联。
        # 比较简单的办法，邮箱和用户名都用转换成gx账号可用的名称后统一使用。
        # 用户名：unionid
        # 邮箱：unionid@dummy.com

        chars = string.ascii_lowercase + string.digits
        username = 'gxid_' + ''.join(random.choices(chars, k=8))
        return {
            "username": username,
            #"email": f"{username}@dummy.com"
        }

    def get_user_id(self, details, response):
        return response.get(self.ID_KEY)
