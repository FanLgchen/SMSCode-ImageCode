



from utils.captcha import captcha



"""生成图形验证码类"""
class ImageCodeView(object):
    """图形验证码"""

    def __init__(self,uuid):

        self.uuid =uuid

    def get(self,uuid):
        """
        :param uuid: 唯一标识
        :return: image/jpg
        """
        #生成图片验证码
        text, image =captcha.generate_captcha()

        #保存图片,一般保存在redis数据库
        redis_conn =get_redis_connection('verify_code')

        redis_conn.setex('img_%s' % uuid, 60, text)

        #响应图片验证码
        return image



