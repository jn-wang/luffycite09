# 作者        :   Administrator 
# 创建时间    :   2019/5/7 0007
# 文件        :   16:44
# IDE         :   PyCharm
import redis
import json
from django.conf import settings
conn = redis.Redis(host='118.24.21.110', port=6379, password='asdf1234')

# conn.flushall()
print(conn.keys())
# # print(conn.hgetall('shopping_car_1_1'))
# print(conn.hget('shopping_car_1_1','title'))
# title = conn.hget('shopping_car_1_1','title')
# print(str(title,encoding='utf-8'))
#
# print(conn.hget('shopping_car_1_1','img'))
#
# print(conn.hget('shopping_car_1_1','policy'))
# policy = conn.hget('shopping_car_1_1','policy')
# print(json.loads(str(policy,encoding='utf-8')))
#
# print(conn.hget('shopping_car_1_1','default_policy'))
# for key in conn.scan_iter("shopping_car_1*"):
#     title = conn.hget(key,'title')
#     img = conn.hget(key,'img')
#     policy = conn.hget(key,'policy')
#     default_policy = conn.hget(key,'default_policy')
#     print(str(title,encoding='utf-8'))
#     print(str(img,encoding='utf-8'))
#     print(json.loads(str(policy,encoding='utf-8')))
#     print(str(default_policy,encoding='utf-8'))
#     print(conn.keys())
# payment_key_list = conn.keys("payment_key_1_*")
# conn.delete(*payment_key_list)
# print(conn.keys())
#
#
# for key in conn.scan_iter():
#     coupon = conn.hget(key, 'coupon')
#     print(coupon)

# global_coupon_dict = {
#    "coupon": {"7": {"money_equivalent_value": 100},"8": {"money_equivalent_value": 50} },
#    "default_coupon": 0
# }
#
# conn.hmset("payment_coupon_key_1",global_coupon_dict)

# course_list = []
# for key in conn.scan_iter('payment_coupon_key_1'):
#     info = {
#         "title" : conn.hget(key, 'title').decode('utf-8'),
#         "img" : conn.hget(key, 'img').decode('utf-8'),
#         "policy" : conn.hget(key, 'policy').decode('utf-8'),
#         "default_policy" : conn.hget(key, 'default_policy').decode('utf-8'),
#         }
#     course_list.append(info)
# print(course_list)
# gcoupon_key = settings.PAYMENT_COUPON_KEY %("1",)
# for key in conn.scan_iter('payment_coupon_key_1'):
#     coupon = conn.hget(key, 'coupon')
