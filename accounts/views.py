import json 
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from accounts.models import UserAuthToken
from accounts.utils import api_authentication
from django.http import HttpResponse, JsonResponse

# Create your views here.



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def send_json(request):

    data = [{'name': 'Peter', 'email': 'peter@example.org'},
            {'name': 'Julia', 'email': 'julia@example.org'}]
    
    data = {'name': 'Peter', 'email': 'peter@example.org'}

    return JsonResponse(data, safe=False)

@csrf_exempt
def login_request(request):
    if request.method == 'POST':
        data = request.POST

        username = request.POST.get('username',"")
        password = request.POST.get('password',"")
        # import pdb; pdb.set_trace()
        if not username or not password:
            response = {
                'username': username if username else 'Field Required',
                'password': '' if password else 'Field Required',
            }
            return JsonResponse(response, safe=True, status=400)

        user_obj = authenticate(username=username, password=password)
        if user_obj:

            obj, created = UserAuthToken.objects.get_or_create(
                user=user_obj,
                defaults={'token':UserAuthToken.generate_unique_key()},
            )

            response = {'success': True, 'token': obj.token }
            return JsonResponse(response, safe=True)
        else:
            response = {'success': False, 'error': 'Invalid credentials.'}
            return JsonResponse(response, safe=True, status=400)

    else:
        return JsonResponse({}, safe=True, status=405)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = request.POST
        first_name = request.POST.get('first_name',"")
        last_name = request.POST.get('last_name',"")
        email = request.POST.get('email',"")
        username = request.POST.get('username',"")
        password = request.POST.get('password',"")

        if not username or not password or not first_name or not email:
            response = {
                'username': username if username else 'Field Required',
                'password': '' if password else 'Field Required',
                'first_name': first_name if password else 'Field Required',
                'email': email if password else 'Field Required',
            }
            return JsonResponse(response, safe=True, status=400)
        else:
            kwargs = {'username': username, 'email': email, 'first_name': first_name, 'password': password,'last_name': last_name}
            if User.objects.filter(username=username).exists():
                response = {'status': False, 'error':'username already exists'}
                return JsonResponse(response, safe=True, status=400)
                
            user = User.objects.create(**kwargs)
            user.set_password(kwargs['password'])
            user.save()
            
            # token = UserAuthToken.generate_unique_key()
            userauth = UserAuthToken.objects.create(token=UserAuthToken.generate_unique_key(), user=user)

            response = {'success': True, 'username':user.username, 'token': userauth.token}
            return JsonResponse(response, safe=True, status=200)


@csrf_exempt
@api_authentication
def myprofile(request):
    user = request.user
    response = {'success': True, 'username':user.username, 'email':user.email, 'first_name':user.first_name, 'last_name':user.last_name }
    return JsonResponse(response, safe=True, status=200)
    