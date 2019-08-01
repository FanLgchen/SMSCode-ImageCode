

"""短信验证码接口"""


import random

from utils.yuntongxun.ccp_sms import CCP


class SMSCodeView(object):

    """短信验证"""

    def get(self,mobile,uuid,image_code):
        """
        :param mobile: 手机号

        """

        #创建连接到redis对象
        redis_conn = get_redis_connection('verify_code')

        #提取图形验证码(保存在redis的)
        image_code_server = redis_conn.get('img_%s' %uuid)


        # 提取校验send_flag
        send_flag =redis_conn.get('send_flag_%s'%mobile)
        if send_flag :

            return '发送短信过于频繁'

        if image_code_server is None:

            return '图形验证码失效'

        #删除图形验证码，避免恶意测试
        try :
            redis_conn.delete('img_%s' %uuid)

        except Exception as e:

            #通过日志打印错误信息
            logger.error(e)


        #对比图形验证码
        image_code_server = image_code_server.decode()

        #转小写后生效
        if image_code.lower() !=image_code_server.lower():
            return '输入图形验证码有误'

        #生成短信验证码
        sms_code ='%06d' %random.randint(0,999999)


        """管道保存代码优化"""

        #创建redis管道
        pl = redis_conn.pipeline()
        # 放入管道一次链接并一起保存
        pl.setex('sms_code_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 执行
        pl.execute()


        #发送短信验证码(重复发送)
        CCP().send_template_sms(mobile,[sms_code,5],constants.SEND_SMS_TEMPLATE_ID)


        #响应结果
        return '发送短信成功'