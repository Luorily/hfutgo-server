from utils.response import get_json_response
from django.views import View


class OldFound(View):
    def get(self, request, stu, user):
        data = stu.request('/http-8080/77726476706e69737468656265737421e0f4408e237e60566b1cc7a99c406d3657/'
                           'accountunlose.action?account=%s&passwd=%s&captcha=%s' % (
                               user.card_id, request.GET['password'], request.GET['code'])).json()
        return get_json_response({
            'status': (data['error'] == 'δΊ€ζζε'),
            'message': data['error']
        })
