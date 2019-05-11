import json
from api import models
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.viewsets import ViewSetMixin

from django_redis import get_redis_connection
from api.utils.exception import PricePolicyInvalid
from api.utils.response import BaseResponse
from api.auth.auth import TmAuth
from django.conf import settings


USER_ID = 1

class ShoopingCarViewSet(APIView):

    authentication_classes = [TmAuth, ]
    conn = get_redis_connection('default')
    def post(self,request,*args,**kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:将商品添加进购物车
        """
        ret = BaseResponse()
        try:
            # 1.获取用户提交的课程ID与价格策略ID
            course_id = int(request.data.get('courseid'))
            policy_id = int(request.data.get('policyid'))
            #2. 获取专题课信息
            course = models.Course.objects.get(id=course_id)
            #3. 获取该课程的所有价格策略
            price_policy_list=course.price_policy.all()
            price_policy_dict={}
            for item in price_policy_list:
                price_policy_dict[item.id]={
                    "period":item.valid_period,
                    "period_display":item.get_valid_period_display(),
                    "price":item.price,
                }
            #4.判断用户提交的价格策略是否合法
            if policy_id not in price_policy_dict:
                raise PricePolicyInvalid('价格策略不合法')
            #5.将购物信息添加到redis中
            car_key = settings.SHOPPING_CAR_KEY %(request.auth.user_id,course_id,)
            car_dict = {
                'title':course.name,
                'img':course.course_img,
                'default_policy':policy_id,
                'policy':json.dumps(price_policy_dict),
            }
            self.conn.hmset(car_key,car_dict)
            ret.data = '添加成功'

        except PricePolicyInvalid as e:
            ret.code=1003
            ret.error=e.msg
        except ObjectDoesNotExist as e:
            ret.code=1002
            ret.error='该课程不存在'
        except Exception as e:
            ret.code=1001
            ret.error='加入购物车失败'
        return Response(ret.dict)

    def delete(self,request,*args,**kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:购物车删除
        """
        ret = BaseResponse()
        try:
            course_id_list = request.data.get('courseids')
            key_list = [settings.SHOPPING_CAR_KEY % (request.auth.user_id, course_id) for course_id in course_id_list]
            # key_list =[]
            # for course_id in course_id_list:
            #     # print(course_id,type(course_id))
            #     key = settings.SHOPPING_CAR_KEY %(request.auth.user_id,course_id)
            #     # print(key)
            #     key_list.append(key)
            self.conn.delete(*key_list)
        except Exception as e:
            ret.code=1002
            ret.error='删除失败'
        return Response(ret.dict)

    def patch(self,request,*args,**kwargs):
        print(request.data)
        ret = BaseResponse()
        try:
            # 获取价格策略ID和课程ID
            course_id = str(request.data.get('courseid'))
            policy_id = str(request.data.get('policyid'))
            # 拼接课程的key
            key = settings.SHOPPING_CAR_KEY % (request.auth.user_id, course_id,)
            if not self.conn.exists(key):
                ret.code = 1001
                ret.error = '课程不存在'
                return Response(ret.dict)

            # reids中获取所有的价格策略
            policy_dict = json.loads(str(self.conn.hget(key,'policy'),encoding='utf-8'))
            print(policy_dict)
            if policy_id not in policy_dict:
                ret.code=1002
                ret.error = '价格策略不合法'
                return Response(ret.dict)

            #开始修改课程的默认价格策略
            self.conn.hset(key,'default_policy',policy_id)
            ret.data = '修改成功'
        except Exception as e:
            ret.code=1003
            ret.error='修改失败'
        return Response(ret.dict)

    def get(self,request,*args,**kwargs):
        ret = BaseResponse()
        try:
            current_user_id = request.auth.user_id
            key_match = settings.SHOPPING_CAR_KEY %(request.auth.user_id,"*")
            course_list = []
            for key in self.conn.scan_iter(key_match,count=10):
                # course_info = self.conn.hgetall(key)
                # print(course_info )
                info = {
                    "title" : self.conn.hget(key, 'title').decode('utf-8'),
                    "img" : self.conn.hget(key, 'img').decode('utf-8'),
                    "policy" : self.conn.hget(key, 'policy').decode('utf-8'),
                    "default_policy" : self.conn.hget(key, 'default_policy').decode('utf-8'),
                }
                course_list.append(info)
            ret.data = course_list
        except Exception as e:
            ret.code = 1002
            ret.error = '获取失败'
        return Response(ret.dict)
#
# class ShoopingCarView(ViewSetMixin, APIView):
#     def list(self, request, *args, **kwargs):
#
#         ret = {'code': 10000, 'data': None, 'error': None}
#         try:
#             shopping_car_course_list = []
#             pattern = settings.LUFFY_SHOPPING_CAR % (USER_ID, '*',)
#
#             user_key_list = CONN.keys(pattern)
#             for key in user_key_list:
#                 temp = {
#                     'id': CONN.hget(key, 'id').decode('utf-8'),
#                     'name': CONN.hget(key, 'name').decode('utf-8'),
#                     'img': CONN.hget(key, 'img').decode('utf-8'),
#                     'default_price_id': CONN.hget(key, 'default_price_id').decode('utf-8'),
#                     'price_policy_dict': json.loads(CONN.hget(key, 'price_policy_dict').decode('utf-8'))
#                 }
#                 shopping_car_course_list.append(temp)
#
#             ret['data'] = shopping_car_course_list
#         except Exception as e:
#             ret['code'] = 1001
#             ret['error'] = '获取购物车数据失败'
#
#         return Response(ret)
#
#     def create(self, request, *args, **kwargs):
#         course_id = request.data.get('courseid')
#         policy_id = request.data.get('policyid')
#
#         course = models.Course.objects.filter(id=course_id).first()
#         if not course:
#             return Response({'code': 10001, 'error': '课程不存在'})
#
#         price_policy_queryset = course.price_policy.all()
#         price_policy_dict = {}
#         for item in price_policy_queryset:
#             temp = {
#                 'id': item.id,
#                 'price': item.price,
#                 'valid_period': item.valid_period,
#                 'valid_period_display': item.get_valid_period_display()
#             }
#             price_policy_dict[item.id] = temp
#         if policy_id not in price_policy_dict:
#             return Response({'code': 10002, 'error': '傻×，价格策略别瞎改'})
#
#         pattern = settings.LUFFY_SHOPPING_CAR % (USER_ID, '*',)
#         keys = CONN.keys(pattern)
#         if keys and len(keys) >= 1000:
#             return Response({'code': 10009, 'error': '购物车东西太多，先去结算再进行购买..'})
#
#         key = settings.LUFFY_SHOPPING_CAR % (USER_ID, course_id,)
#         CONN.hset(key, 'id', course_id)
#         CONN.hset(key, 'name', course.name)
#         CONN.hset(key, 'img', course.course_img)
#         CONN.hset(key, 'default_price_id', policy_id)
#         CONN.hset(key, 'price_policy_dict', json.dumps(price_policy_dict))
#
#         return Response({'code': 10000, 'data': '购买成功'})
#
#     def destroy(self, request, *args, **kwargs):
#
#         response = BaseResponse()
#         try:
#             courseid = request.GET.get('courseid')
#             key = settings.LUFFY_SHOPPING_CAR % (USER_ID, courseid,)
#
#             CONN.delete(key)
#             response.data = '删除成功'
#         except Exception as e:
#             response.code = 10006
#             response.error = '删除失败'
#         return Response(response.dict)
#
#     def update(self, request, *args, **kwargs):
#
#         response = BaseResponse()
#         try:
#             course_id = request.data.get('courseid')
#             policy_id = str(request.data.get('policyid')) if request.data.get('policyid') else None
#
#             key = settings.LUFFY_SHOPPING_CAR % (USER_ID, course_id,)
#
#             if not CONN.exists(key):
#                 response.code = 10007
#                 response.error = '课程不存在'
#                 return Response(response.dict)
#
#             price_policy_dict = json.loads(CONN.hget(key, 'price_policy_dict').decode('utf-8'))
#             if policy_id not in price_policy_dict:
#                 response.code = 10008
#                 response.error = '价格策略不存在'
#                 return Response(response.dict)
#
#             CONN.hset(key, 'default_price_id', policy_id)
#             CONN.expire(key, 20 * 60)
#             response.data = '修改成功'
#         except Exception as e:
#             response.code = 10009
#             response.error = '修改失败'
#
#         return Response(response.dict)
