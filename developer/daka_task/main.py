import os, sys
parent_path = os.path.abspath('.')
sys.path.append(parent_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hfutgo.settings")
import django
django.setup()

import requests, re, json
from datetime import time, datetime
from enum import Enum
from developer.daka_task.Student import Student
from utils.ECBPkcs7 import ECBPkcs7
from config import UserInfo
from developer.models import DakaLog

class Url(Enum):
    key = 'http://stu.hfut.edu.cn/xsfw/sys/emapfunauth/pages/funauth-login.do'
    login = 'http://stu.hfut.edu.cn/xsfw/sys/emapfunauth/loginValidate.do'
    initialize = 'http://stu.hfut.edu.cn/xsfw/sys/swpubapp/indexmenu/getAppConfig.do?appId=5811258723206966&appName=xsyqxxsjapp'
    date = 'http://stu.hfut.edu.cn/xsfw/sys/xsyqxxsjapp/mrbpa/getDateTime.do'
    time = 'http://stu.hfut.edu.cn/xsfw/sys/xsyqxxsjapp/mrbpa/getTsxx.do'
    jbxx = 'http://stu.hfut.edu.cn/xsfw/sys/xsyqxxsjapp/mrbpa/getJbxx.do'
    zxpaxx = 'http://stu.hfut.edu.cn/xsfw/sys/xsyqxxsjapp/mrbpa/getZxpaxx.do'
    save = 'http://stu.hfut.edu.cn/xsfw/sys/xsyqxxsjapp/mrbpa/saveMrbpa.do'


class Daka:
    __headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }

    def __init__(self):
        self.__student = Student()

    def __getCryptoKey(self):
        data = self.__student.request(Url.key.value).text
        regexp = r'cryptoKey = "(.*)"'
        key = re.findall(regexp, data)[0]
        return key

    def __encryptPwd(self, password):
        key = self.__getCryptoKey()
        return ECBPkcs7(key).encrypt(password)

    def __login(self, id, password):
        return self.__student.login(id, password)

    def __initialize(self):
        data = self.__student.request(Url.initialize.value)

    def __getZxpaxx(self):
        data = self.__student.request(
            url=Url.zxpaxx.value,
            method='POST',
            headers=self.__headers,
            data={'data': '{}'}
        ).json()
        if data['code'] == '0':
            return data['data']
        else:
            return False

    def __getJbxx(self):
        data = self.__student.request(
            url=Url.jbxx.value,
            method='POST',
            headers=self.__headers,
            data={'data': '{}'}
        ).json()
        if data['code'] == '0':
            return data['data']
        else:
            return False

    def __getDate(self):
        data = self.__student.request(
            url=Url.date.value,
            method='POST',
            headers=self.__headers,
            data={'data': '{}'}
        ).json()
        return data['data']['DQRQ']

    def __getTime(self):
        data = self.__student.request(
            url=Url.time.value,
            method='POST',
            headers=self.__headers,
            data={'data': '{}'}
        )
        data = data.json()
        class Time:
            def __init__(self, start, end):
                start = re.findall(r'([0-9]{2})', start)
                end = re.findall(r'([0-9]{2})', end)
                self.start = time(hour=int(start[0]), minute=int(start[1]), second=int(start[2]))
                self.end = time(hour=int(end[0]), minute=int(end[1]), second=int(end[2]))

        return Time(data['data']['DZ_TBKSSJ'], data['data']['DZ_TBJSSJ'])

    def __save(self):
        zxpaxx = self.__getZxpaxx()
        jbxx = self.__getJbxx()
        data = {
            'data': json.dumps({
                'JBXX': json.dumps(jbxx),
                'MRQK': json.dumps({
                    'WID': '',
                    'XSBH': '',
                    'DZ_TBDZ': '',
                    'TW': '',
                    'BRJKZT': '',
                    'SFJZ': '',
                    'JTCYJKZK': '',
                    'XLZK': '',
                    'QTQK': '',
                    'TBSJ': self.__getDate(),
                    'DZ_SFSB': '1',
                    'BY1': '1',
                    **zxpaxx
                })
            })
        }
        data = self.__student.request(
            url=Url.save.value,
            method='POST',
            headers=self.__headers,
            data=data
        ).json()
        if data['code'] == '0':
            return True
        else:
            return data['msg']

    def run(self, id, password):
        try:
            logined = self.__login(id, password)
        except requests.exceptions.RequestException:  # ???HFUT??????????????????
            return "????????????????????????????????????"
        except:
            return "????????????????????????????????????"
        if logined is True:
            print("????????????")
            self.__initialize()
            times = self.__getTime()
            now = datetime.now()
            now = time(hour=now.hour, minute=now.minute, second=now.second)
            print('???????????????', times.start)
            print('???????????????', times.end)
            if (now < times.end) and (now > times.start):
                saved = self.__save()
                if saved == True:
                    return '????????????'
                else:
                    return '???????????????' + saved
            else:
                return '???????????????????????????'
        else:
            return '????????????????????????'


if __name__ == '__main__':
    for user in UserInfo.users.value:
        if user['enable']:
            daka = Daka()
            print("???????????????" + user['user'])
            status = daka.run(user['user'], user['password'])
            print(status)
            DakaLog(user=user['user'], status=1, log=status).save()
