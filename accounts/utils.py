from django.http import HttpResponse
from accounts.models import UserAuthToken


class HttpResponseUnauthorized(HttpResponse):
    # data = {'token': 'Invalid token'}
    status_code = 401 


def api_authentication(func):
    def inner(request, *args, **kwargs):
        deco_token =  request.META.get('HTTP_AUTHORIZATION')
        userauth_obj = UserAuthToken.objects.filter(token=deco_token)
        if not userauth_obj:
            return HttpResponseUnauthorized()

        request.user = userauth_obj[0].user
        return func(request, *args, **kwargs)
    return inner