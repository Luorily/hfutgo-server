from utils.response import get_json_response
from django.views import View
import requests


class Haier(View):
    def get(self, request):
        mid = request.GET['mid']
        ssid = request.GET['ssid']
        data = requests.get('https://www.saywash.com/saywash/WashCallApi/common/laundry/getDeviceInfo.api',
                            params={
                                'deviceQRCode': mid,
                                'ssid': ssid
                            }).json()['data']
        if data['status'] == 1:
            status = '空闲'
        elif data['status'] == 2:
            status = '使用中，剩余' + data['timeRemaining'] + '分钟'
        else:
            status = '未知'
        return get_json_response({
            'status': status
        })
