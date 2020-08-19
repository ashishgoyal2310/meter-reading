from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate

from users.forms import UserCreateForm
from email_task import send_user_register_email
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
User = get_user_model()


def get_random_string():
    import random
    import string
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(10))
    return result_str


# Create your views here.
@login_required
def users_index(request):
    template_name = "blank.html"
    ctx = {}
    return render(request, template_name, ctx)


def users_login(request):
    template_name = "users/users_login.html"
    if request.method == 'POST':
        print(request.POST)
        email = data.POST('email')
        password = data.POST('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            return redirect('/users/')
        else:
            note = 'Invalid credentials'
            return render(request, template_name,{'note':note})
    
    return render(request, template_name)

        # if not email or not password:
        #     return render(request, template_name)

    # template_name = "users/user_login.html"
    # ctx = {}
    # return render(request, template_name, ctx)

@login_required
@permission_required('auth.view_user', raise_exception=True)
def user_list_view(request):
    template_name = "users/user_list.html"
    all_users = User.objects.all()
    ctx = {'all_users': all_users}
    return render(request, template_name, ctx)

@login_required
@permission_required('auth.add_user', raise_exception=True)
def user_create_view(request):
    template_name = "users/user_create.html"
    ctx = {}
    RANDOM_PWD = get_random_string()

    if request.method == 'POST':
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(RANDOM_PWD)
            user.save()
            form = UserCreateForm()
            ctx['message'] = "User '{}' created successfully.".format(user.username)
            send_user_register_email(user, RANDOM_PWD)
    else:
        form = UserCreateForm()

    ctx['form'] = form
    return render(request, template_name, ctx)