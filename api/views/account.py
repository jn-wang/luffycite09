import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
from django.shortcuts import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from api.utils.response import TokenResponse
"""
    用于用户认证相关接口
"""
class AuthView(APIView):
    def post(self,request,*args,**kwargs):
        ret = TokenResponse()
        try:
            user = request.data.get('user')
            pwd = request.data.get('pwd')
            user_list = models.UserInfo.objects.get(username=user,pwd=pwd)
            if not user_list:
                ret.code=1001
                ret.error='用户名或密码错误'
                return Response(ret.dict)
            uid = str(uuid.uuid4())
                # 更新或创建token
            models.UserToken.objects.update_or_create(user_id=user_list[0].id,defaults={'token':uid})
            ret.token = uid
        # except ObjectDoesNotExist as e:
        #     ret['code'] = 1002
        #     ret['error']='该用户不存在'
        except Exception as e:
            ret.code = 1003
        return Response(ret.dict)

"""
    用于用户注册相关接口
"""
class RegisteredView(APIView):
    def post(self,request,*args,**kwargs):
        ret = TokenResponse()
        try:
            user = request.data.get('user')
            pwd = request.data.get('pwd')
            email = request.data.get('email')
            tel = request.data.get('tel')
            models.UserInfo.objects.create(username=user,pwd=pwd,email=email,tel=tel)
        except Exception as e:
            ret.code = 1003
        return Response(ret.dict)

