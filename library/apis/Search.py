from utils.response import get_json_response
from django.views import View
import json


class Search(View):
    def post(self, request, stu):
        filters = json.loads(request.body)['filters']
        data = stu.request(
            '/http-8080/77726476706e69737468656265737421a2a611d2736526022a5ac7f9/opac/ajax_search_adv.php',
            method='POST',
            headers={
                'Content-Type': 'application/json'
            },
            data={
                "searchWords": [
                    {
                        "fieldList": [
                            {
                                "fieldCode": "any",
                                "fieldValue": request.GET['word']
                            }
                        ]
                    }
                ],
                "filters": filters,
                "limiter": [],
                "sortField": "relevance",
                "sortType": "desc",
                "pageSize": 20,
                "pageCount": int(request.GET['page']),
                "locale": "zh_CN",
                "first": True
            }).json()
        return get_json_response(data)
