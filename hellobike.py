import requests, json, os, sys, time, base64, datetime, random
import matplotlib.pyplot as plt  # plt 用于显示图片
import matplotlib.image as mpimg  # mpimg 用于读取图片
# % matplotlib inline

import numpy as np

session = requests.session()
headers = {"Accept": "application/json, text/plain, */*", "Accept-Encoding": "br, gzip, deflate",
           "Accept-Language": "zh-cn", "Connection": "keep-alive", "Content-Length": "131",
           "Content-Type": "text/plain;charset=UTF-8", "Host": "api.ttbike.com.cn", "Origin": "http://m.ttbike.com.cn",
           "Referer": "http://m.ttbike.com.cn/ebike-h5/latest/index.html",
           "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 MQQBrowser/8.8.2 Mobile/16A5345f Safari/604.1 MttCustomUA/2 QBWebViewType/1 WKType/1"}


def sendSMSCode(phone):
    '''
    功能：输入手机号，模拟完成获取短信验证码的操作。
    1.传入手机号phone
    2.如果顺利，请求响应会包含base64图片验证码，否则显示异常信息
    3.显示图片验证码，弹框要求输入。如果输入的验证码正确，服务器会返回发送短信成功的响应，否则显示异常信息
    '''
    get_code_url = 'https://api.ttbike.com.cn/auth?user.account.sendCodeV2'
    get_code_data = {"version": "4.2.3", "from": "h5", "systemCode": 63, "platform": 6,
                     "action": "user.account.sendCodeV2", "mobile": "", "capText": ""}
    get_code_data["mobile"] = phone
    r = session.post(get_code_url, headers=headers, data=json.dumps(get_code_data), timeout=6)  # post手机号
    status = False
    if "imageCaptcha" in r.text:  # 获取短信验证码前需要验证图片验证码，如果response包含验证码字段，则正确，否则异常
        img = json.loads(r.text)["data"]["imageCaptcha"]
        with open("captcha.png", 'wb') as tempout:
            tempout.write(base64.decodebytes(bytes(img[22:], "utf-8")))  # 将base64图片验证码解码保存
        captcha = mpimg.imread('captcha.png')  # 使用mpimg读取验证码
        plt.imshow(captcha)  # 在Ipython或JupyterNoetebook显示图片，便于人工输入
        plt.axis('off')
        plt.show()
        code = input('请输入图片验证码:')
        get_code_data["capText"] = code
        r = session.post(get_code_url, headers=headers, data=json.dumps(get_code_data), timeout=6)
        if 'true' in r.text:
            print(r.text)
            print('短信验证码发送成功！')
            status = True
        else:
            print('图片验证码错误！')
    else:
        print(r.text)
    return status


def getToken(phone, code):
    '''
    功能：输入手机号和短信验证码，模拟用户登陆，获取token
    1.传入手机号和对应的短信验证码
    2.如果登陆成功，返回token，否则显示异常信息
    '''
    login_url = 'https://api.ttbike.com.cn/auth?user.account.login'
    login_data = {"version": "4.2.3", "from": "h5", "systemCode": 63, "platform": 1, "action": "user.account.login",
                  "mobile": "", "code": "", "picCode": {"cityCode": "0517", "city": "淮安市", "adCode": "223001"}}
    login_data["mobile"] = phone
    login_data["mobile"] = phone
    login_data["code"] = code
    r = session.post(login_url, headers=headers, data=json.dumps(login_data), timeout=6)
    token = json.loads(r.text)["data"]["token"]
    print('获取token成功')
    return token


def getBikes(lng, lat, token):
    '''
    功能：获取某一经纬度周边500米的所有单车信息
    1.传入经纬度和token值
    2.如果顺利，返回经纬度周围500米的所有单车信息，否则显示异常信息
    '''
    get_bike_data = {"version": "4.2.3", "from": "h5", "systemCode": 63, "platform": 1, "action": "user.ride.nearBikes",
                     "lat": '', "lng": '', "cityCode": "0517", "currentLng": '', "currentLat": '', "adCode": "223001",
                     "token": ""}
    get_bike_data["currentLat"] = get_bike_data["lat"] = lat  # 纬度 32
    get_bike_data["currentLng"] = get_bike_data["lng"] = lng  # 经度 118
    get_bike_data["token"] = token
    get_bike_url = 'https://api.ttbike.com.cn/api?user.ride.nearBikes'
    bikesr = requests.post(get_bike_url, headers=headers, data=json.dumps(get_bike_data), timeout=20)
    if 'bikeNo' in bikesr.text:
        return json.loads(bikesr.text)["data"]
    else:
        print(bikesr.text)


def getPhone():
    '''
    功能：利用某接码平台，获取手机号
    1.利用某接码平台的API，获取手机号用于哈啰单车登陆，其中token为接码平台用户token
    2.如果顺利，返回获取的手机号，否则显示异常信息
    '''
    getphone_url = "http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=*******************&itemid=25342"
    r = requests.get(getphone_url)
    if "success" in r.text:
        return r.text.split('|')[-1]
    else:
        print('获取失败：', r.text)
        return ""


def releasePhone(phone):
    '''
    功能：释放指定手机号
    1.手动释放获取的手机号（用于图片验证码输入错误等中断情况，正常情况会自动释放）
    2.如果顺利，显示成功，否则显示异常信息
    '''
    releasephone_url = "http://api.fxhyd.cn/UserInterface.aspx?action=release&token=************1&itemid=25342&mobile=%s" % phone
    r = requests.get(releasephone_url)
    if "success" in r.text:
        print("释放成功！")
    else:
        print('释放失败：', r.text)


def getSMScode(phone):
    '''
    功能：获取指定手机号收到的短信
    1.获取某手机号接收到的短信
    2.如果顺利，提取短信中的验证码并返回，否则显示异常信息
    '''
    getSMS_url = "http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token=************************&itemid=25342&release=1&mobile=%s" % phone
    r = requests.get(getSMS_url)
    r.encoding = r.apparent_encoding
    if "success" in r.text:
        return r.text.split(':')[-1].split(',')[0].strip()
    else:
        return ""


def saveTokens(nums=25):
    '''
    构建token池
    1.token池以文本文档形式存储
    2.读取token池，当token池内token的数量小于预设值时，自动获取token。
    3.自动模拟登陆的所有流程，用户只需要输入展示的图片验证码。
    '''
    token_list = []
    with open("tokens.txt", 'r', encoding="utf-8") as f:
        token_list = list(set(f.read().split('\n')))
    if len(token_list) < nums:
        while len(token_list) < nums:
            clean = os.system('clear')
            print('当前token池数量%s' % len(token_list))
            phone = getPhone()
            print('获取手机号成功%s' % phone)
            try:
                if sendSMSCode(phone):
                    time.sleep(5)
                    SMScode = getSMScode(phone)
                    count = 0
                    while SMScode == "" and count < 20:
                        count += 1
                        print('第%s次获取验证码' % count, end='\r')
                        SMScode = getSMScode(phone)
                        time.sleep(5)
                    if SMScode != "":
                        print('短信验证码为：%s' % SMScode)
                        new_token = getToken(phone, SMScode)
                        print(new_token)
                        token_list.append(new_token)
                    else:
                        print("%s短信验证码提取失败" % phone)
                        releasePhone(phone)
                else:
                    print("%s验证码错误" % phone)
                    releasePhone(phone)  # 遇到异常情况，自动释放手机号
            except:
                releasePhone(phone)  # 遇到异常情况，自动释放手机号
                with open("tokens.txt", 'a+', encoding="utf-8") as f:
                    f.write('\n'.join(token_list))
                break
        with open("tokens.txt", 'w', encoding="utf-8") as f:
            f.write('\n'.join(token_list))
    print('token池数量目标值%s,实际值%s，停止获取token' % (nums, len(token_list)))


def getAllBikes():
    '''
    获取南京大学仙林校区范围内的所有单车数据
    1.将南京大学仙林校区划分为N个方格
    2.每次获取单车数据轮流采用不同的token，以防止被封。
    3.自动从token池中移除被封的token。
    4.获取每个方格交界点周边的单车数据
    5.对所有获取到的数据进行去重
    '''
    token_list = []
    with open("tokens.txt", 'r', encoding="utf-8") as f:
        token_list = list(set(f.read().split('\n')))
    if len(token_list) == 0:
        raise Exception('tokens为空！')
        return
    lnglist = [i / 100000 for i in range(11903772, 11904656, 170)]  # lng坐标，只需要改前两个
    latlist = [i / 100000 for i in range(3354852, 3356116, 170)]  # lat坐标，只需要改前两个,170/100000大概是500米的间隔
    print('一共', len(lnglist) * len(latlist), '个点')
    allbikes = []
    count = 1
    for i in latlist:
        for j in lnglist:
            try:
                token_i = count % len(token_list)
                print('token:' + str(token_i) + '正在加载第' + str(count) + '个点:' + str(j) + '---' + str(i), end='\r')
                allbikes = allbikes + getBikes(j, i, token_list[token_i])
                count += 1
                time.sleep(1)
            except TypeError:
                print('第', count, '出错，删除过期token')
                token_list.pop(token_i)
                token_i = random.randint(0, len(token_list))
                allbikes = allbikes + getBikes(j, i, token_list[token_i])
    with open("tokens.txt", 'w', encoding="utf-8") as f:
        f.write("\n".join(token_list))
    return allbikes


def writeRes(allbikes, timestamp):
    '''
    功能：将单车数据追加写入文本文件存储

    '''
    duplicated_bikes = []
    for bike in allbikes:
        if bike not in duplicated_bikes:
            duplicated_bikes.append(bike)
    with open('allBikes.txt', 'a+') as f:
        for bike in duplicated_bikes:
            f.write(str(timestamp) + '\t')
            f.write(('\t'.join([bike['bikeNo'], bike['lat'], bike['lng']])))
            f.write('\n')
        print(timestamp + 'write done.')


def run():
    '''
    功能：每隔两分钟获取一次南京大学仙林校区的所有单车信息并保存。

    '''
    # saveTokens(20)
    while (True):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            nexttime = (datetime.datetime.now() + datetime.timedelta(minutes=2))
            print(timestamp)
            allbikes = getAllBikes()
            writeRes(allbikes, timestamp)
            resttime = (nexttime - datetime.datetime.now()).seconds
            time.sleep(resttime)
        except KeyboardInterrupt:
            break




if __name__ == "__main__":
    run()  # 测试函数
    # run()
