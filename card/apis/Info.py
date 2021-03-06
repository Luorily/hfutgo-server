from utils.response import get_json_response
from bs4 import BeautifulSoup
from django.views import View
from utils.Student import Student
import re


class Info(View):
    def get(self, request, stu: Student, user):
        try:
            stu.request('http://172.31.248.20/ahdxdrPortalHome.action', timeout=7)
            data = stu.request(
                'http://172.31.248.20/accountcardUser.action').text
            soup = BeautifulSoup(data, 'lxml').select('.tttt > tr:nth-child(1) > th:nth-child(1) > table:nth-child(1)')[0]
            balance_text = soup.select('tr:nth-child(12) > td:nth-child(2)')[0].text
            balance_data = re.match(r'(.*)元（卡余额）(.*)元\(当前过渡余额\)(.*)元\(上次过渡余额\)', balance_text)
            card_id = soup.select('tr:nth-child(2) > td:nth-child(4) > div:nth-child(1)')[0].text
            if user.card_id is None:
                user.card_id = card_id
                user.save()
            return get_json_response({
                'id': card_id,
                'sum': str(round(float(balance_data[1]) + float(balance_data[2]), 2)),
                'available': balance_data[1],
                'waiting': balance_data[2],
                'freeze': soup.select('tr:nth-child(11) > td:nth-child(6) > div:nth-child(1)')[0].text.strip(),
                'lost': soup.select('tr:nth-child(12) > td:nth-child(6)')[0].text.strip()
            })
        except BaseException as e:
            print(e)
            return get_json_response('学校维护中', 3001)
