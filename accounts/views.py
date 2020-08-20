import json
from email_task import sendSimpleEmail, send_user_register_email, send_forgot_password_email
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from accounts.models import UserAuthToken, UserForgetPassword
from accounts.utils import api_authentication
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import permission_required


# Create your views here.
#ashish - 67f871d24d664506b31b4bee277ad1ee
# requestoruser 34a643e53e3749e1af176e5af3c09ce1
# User8last8 e0cfbb6aa5a7456fa4df4a591f1355bd


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
        data = json.loads(request.body)

        username = data.get('username',"")
        password = data.get('password',"")
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
        data = json.loads(request.body)
        first_name = data.get('first_name',"")
        last_name = data.get('last_name',"")
        email = data.get('email',"")
        username = data.get('username',"")
        password = data.get('password',"")

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
    # email_res = sendSimpleEmail(user)
    response = {'success': True, 'username':user.username, 'email':user.email, 'first_name':user.first_name, 'last_name':user.last_name,'email_res':email_res }
    return JsonResponse(response, safe=True, status=200)


@csrf_exempt
@api_authentication
@permission_required('auth.add_user', raise_exception=True)
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name = data.get('first_name',"")
        last_name = data.get('last_name',"")
        email = data.get('email',"")
        username = data.get('username',"")
        password = data.get('password',"")
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
            password = kwargs['password']
            send_user_register_email(user,password)
            return JsonResponse(response, safe=True, status=200)
        

@csrf_exempt
@api_authentication
@permission_required('auth.view_user', raise_exception=True)
def users_list(request):
    all_users = User.objects.all()
    all_users_list=[]
    for user_obj in all_users:
        response = {
                'id': user_obj.id,
                'first_name':user_obj.first_name,
                'last_name':user_obj.last_name,
                'email': user_obj.email,
                'date_joined': user_obj.date_joined
            }
        all_users_list.append(response)
    return JsonResponse(all_users_list, safe=False, status=200)

@csrf_exempt
def forget_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if not UserForgetPassword.objects.filter(user=user).exists():
                user_forget_pass = UserForgetPassword.objects.create(token=UserAuthToken.generate_unique_key(), user=user)

            forget_password_obj = UserForgetPassword.objects.get(user=user)
            response = {'status': True, 'token':'Email sent for password reset'}
            send_forgot_password_email(user,forget_password_obj.token)
            return JsonResponse(response, safe=True, status=200)

        else:
            response = {'status': False, 'error':'Email does not exist ! Please enter Valid email'}
            return JsonResponse(response, safe=False, status=400)