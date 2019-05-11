# 作者        :   Administrator 
# 创建时间    :   2019/5/7 0007
# 文件        :   15:35
# IDE         :   PyCharm  

# 自定义抛出错误
class PricePolicyInvalid(Exception):
    def __init__(self,msg):
        self.msg = msg