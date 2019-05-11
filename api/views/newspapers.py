# 作者        :   jn-wang
# 创建时间    :   2019/5/7 0007
# 文件        :   10:04
# IDE         :   PyCharm
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from api.auth.auth import TmAuth

class NewPapers(ViewSetMixin,APIView):
    authentication_classes = [TmAuth,]
    def list(self,request,*args,**kwargs):
        # ret = BaseResponse()
        # try:
        #     queryset = models.Artcle
        pass
    def post(self,request,*args,**kwargs):
        pass