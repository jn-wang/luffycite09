# 作者        :   Administrator 
# 创建时间    :   2019/5/8 0008
# 文件        :   17:07
# IDE         :   PyCharm  
import json
import datetime
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

class PayMentViewSet(APIView):
    authentication_classes = [TmAuth,]
    conn = get_redis_connection('default')
    ret = BaseResponse()
    def post(self,request,*args,**kwargs):
        try:
            payment_key_list = self.conn.keys(settings.PAYMENT_KEY %(request.auth.user_id,'*',))
            payment_key_list.append(settings.PAYMENT_COUPON_KEY %(request.auth.user_id))
            self.conn.delete(*payment_key_list)

            global_coupon_dict = {
                "coupon":{},
                "default_coupon":0
            }
            payment_dict = {}
            # 1.根据课程ID去redis中获取相应的课程信息
            couser_id_list = request.data.get('courseids')
            for couser_id in couser_id_list:
                car_key = settings.SHOPPING_CAR_KEY %(request.auth.user_id,couser_id)
                # 检测用户要结算的课程是否已经加入购物车
                if not self.conn.exists(car_key):
                    self.ret.code=1002
                    self.ret.error='需要先将课程添加进购物车'
                # 3.从购物车获取信息，放入至结算中心
                policy = json.loads(self.conn.hget(car_key, 'policy').decode('utf-8'))
                default_policy = self.conn.hget(car_key, 'default_policy').decode('utf-8')
                policy_info = policy[default_policy]
                payment_course_dict = {
                    'couser_id':str(couser_id),
                    'title' : self.conn.hget(car_key, 'title').decode('utf-8'),
                    'img' : self.conn.hget(car_key, 'img').decode('utf-8'),
                    'policy_id':str(couser_id),
                    'coupon':{},
                    'default_policy':0
                }
                payment_course_dict.update(policy_info)
                payment_dict[str(couser_id)] = payment_course_dict

                #根据课程ID 获取选择的价格策略信息
            # self.ret.data=payment_dict
            ctime = datetime.date.today()

            coupon_list = models.CouponRecord.objects.filter(# 取到这个用户拥有的所有优惠卷
                account=request.auth.user,
                status=0, # 领取时间要求大于开始时间，小于结束时间
                coupon__valid_begin_date__lte=ctime,
                coupon__valid_end_date__gte=ctime,
            )
            for item in coupon_list:
                info = {}
                coupon_course_id = str(item.coupon.object_id)  # 优惠卷绑定课程的id
                coupon_id = str(item.id) # 优惠卷ID
                coupon_type = item.coupon.coupon_type #优惠卷类型：满减，折扣，立减

                info['coupon_type'] = coupon_type
                info['coupon_display'] = item.coupon.get_coupon_type_display()
                if not item.coupon.object_id:
                    info = {}
                    info['coupon_type'] = coupon_type
                    info['coupon_display'] = item.coupon.get_coupon_type_display()
                    if coupon_type == 0:  # 立减卷
                        info['money_equivalent_value'] = item.coupon.money_equivalent_value
                    elif coupon_type == 1:  # 满减卷
                        info['money_equivalent_value'] = item.coupon.money_equivalent_value
                        info['minimum_consume'] = item.coupon.minimum_consume
                    else:# 折扣卷
                        info['off_percent'] = item.coupon.off_percent
                    global_coupon_dict["coupon"][coupon_id] = info
                    continue
                if coupon_type == 0:# 立减卷
                    info['money_equivalent_value'] = item.coupon.money_equivalent_value
                elif coupon_type == 1:# 满减卷
                    info['money_equivalent_value'] = item.coupon.money_equivalent_value
                    info['minimum_consume'] = item.coupon.minimum_consume
                else:# 折扣卷
                    info['off_percent'] = item.coupon.off_percent
                if coupon_course_id not in payment_dict:
                    continue

                payment_dict[coupon_course_id]['coupon'][coupon_id] = info

                # 将优惠卷设置到制定的课程中，写入redis中（结算中心）

            for cid,cinfo in payment_dict.items():
                pay_key = settings.PAYMENT_KEY %(request.auth.user_id,cid,)
                cinfo['coupon'] = json.dumps(cinfo['coupon'])
                print(cinfo['coupon'])
                self.conn.hmset(pay_key,cinfo)
                # 将全栈的优惠券写入redis


            gcoupon_key = settings.PAYMENT_COUPON_KEY %(request.auth.user_id,)
            global_coupon_dict['coupon'] = json.dumps(global_coupon_dict['coupon'])
            self.conn.hmset(gcoupon_key,global_coupon_dict)

            self.ret.data=payment_dict
        except Exception as e:
            self.ret.code=1001
            self.ret.error='报错啦'
        return Response(self.ret.dict)

    # 修改优惠券
    def patch(self,request,*args,**kwargs):
        # print(request.data)
        try:
            course = request.data.get('courseid')
            course_id = str(course) if course else course
            coupon_id = str(request.data.get('couponid'))

            redis_global_coupon_key = settings.PAYMENT_COUPON_KEY %(request.auth.user_id,)
            redis_payment_key = settings.PAYMENT_KEY %(request.auth.user_id,course_id,)

            if not course_id:
                # 修改全站优惠券
                if coupon_id == '0':
                    # 不适用优惠券,请求：{"couponid":0}
                    self.conn.hset('payment_global_coupon_1','default_coupon',coupon_id)
                    self.ret.data = "修改成功"
                    return Response(self.ret.dict)
                # 用优惠券,请求：{"couponid":*}
                coupon_dict = json.loads(self.conn.hget(redis_global_coupon_key,'coupon').decode('utf-8'))
                print(coupon_dict)
                #判断用户选择的优惠券是否合法
                if coupon_id not in coupon_dict:
                    self.ret.code = 1001
                    self.ret.error = "优惠券不存在"
                    return Response(self.ret.dict)

                gcoupon_key = settings.PAYMENT_COUPON_KEY % (request.auth.user_id,)
                self.conn.hset(redis_global_coupon_key, 'default_coupon', coupon_id)

            if coupon_id == "0":
                self.conn.hset(redis_payment_key,'default_coupon',course_id)
                self.ret.data = "修改成功"
                return Response(self.ret.dict)
            coupon_dict = json.loads(self.conn.hget(redis_payment_key, 'coupon').decode('utf-8'))
            print(coupon_dict)
            if course_id not in coupon_dict:
                self.ret.code = 1003
                self.ret.error = "课程优惠券不存在"
                return Response(self.ret.dict)
            self.conn.hset(redis_payment_key,'default_coupon',course_id)
        except Exception as e:
            self.ret.code = 1002
            self.ret.error = "报错了,修改失败"
        return Response(self.ret.dict)


    def get(self,request,*args,**kwargs):
        try:
            redis_payment_key = settings.PAYMENT_KEY %(request.auth.user_id,"*")
            redis_global_coupon_key = settings.PAYMENT_COUPON_KEY % (request.auth.user_id,)

            # 1.获取绑定的课程信息
            course_list = []
            for key in self.conn.scan_iter(redis_payment_key):
                info = {}
                data = self.conn.hgetall(key)
                for k,v in data.items():
                    kk = k.decode('utf-8')
                    if kk == "coupon":
                        info[kk] = json.loads(v.decode('utf-8'))
                    else:
                        info[kk] = v.decode('utf-8')
                course_list.append(info)
                print(course_list)

            # 全站优惠券
            global_coupon_dict = {
                'coupon':json.loads(self.conn.hget(redis_global_coupon_key,'coupon').decode('utf-8')),
                'default_coupon':self.conn.hget(redis_global_coupon_key,'default_coupon').decode('utf-8')
            }
            # print(global_coupon_dict)

            self.ret.data = {
                'course_list':course_list,
                'global_coupon_dict':global_coupon_dict
            }
        except Exception as e:
            self.ret.code=1001
            self.ret.error='获取优惠券信息错误'
        return Response(self.ret.dict)














