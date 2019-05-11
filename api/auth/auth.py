# 作者        :   Administrator 
# 创建时间    :   2019/5/7 0007
# 文件        :   认证相关模块
# IDE         :   PyCharm
from rest_framework.authentication import BaseAuthentication
from api import models
from rest_framework.exceptions import AuthenticationFailed

class TmAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        obj = models.UserToken.objects.filter(token=token).first()
        if not obj:
            raise AuthenticationFailed({'code':1001,'error':'认证失败'})
        return (obj.user.username,obj)