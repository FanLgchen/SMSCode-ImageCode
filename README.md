# SMSCode-ImageCode
在项目里实现图形验证码及短信验证码方案的Demo及使用说明
##　图形验证码
### 准备 captcha 扩展包
* pip install Pillow
### 准备 Redis 数据库
```python
"verify_code": { # 验证码
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": "redis://127.0.0.1:6379/2",
    "OPTIONS": {
        "CLIENT_CLASS": "django_redis.client.DefaultClient",
    }
},
```
### 接口
* 生成图片验证码 text, image = captcha.generate_captcha()
* 保存图片验证码 redis_conn = get_redis_connection('verify_code')

## 短信验证码
### 容联云通讯短信平台
* 申请开发者https://www.yuntongxun.com/　
* 模板短信SDK测试
```python
from verifications.libs.yuntongxun.CCPRestSDK import REST

# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
_accountSid = '8aaf070862181ad5016236f3bcc811d5'

# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = '4e831592bd464663b0de944df13f16ef'

# 请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = '8aaf070868747811016883f12ef3062c'

# 说明：请求地址，生产环境配置成app.cloopen.com
_serverIP = 'sandboxapp.cloopen.com'

# 说明：请求端口 ，生产环境为8883
_serverPort = "8883"

# 说明：REST API版本号保持不变
_softVersion = '2013-12-26'

# 云通讯官方提供的发送短信代码实例
# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id
def sendTemplateSMS(to, datas, tempId):
    # 初始化REST SDK
    rest = REST(_serverIP, _serverPort, _softVersion)
    rest.setAccount(_accountSid, _accountToken)
    rest.setAppId(_appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    print(result)
    for k, v in result.items():

        if k == 'templateSMS':
            for k, s in v.items():
                print('%s:%s' % (k, s))
        else:
            print('%s:%s' % (k, v))

if __name__ == '__main__':
    # 注意： 测试的短信模板编号为1
    sendTemplateSMS('17600992168', ['123456', 5], 1)
```

### 接口
* 提取图形验证码
* 删除，防止恶意测试
* 对比图形验证码
* 生成短信验证码
* 保存短信验证码到redis
* 发送短信验证码



