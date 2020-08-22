from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.urls import reverse_lazy

from users.forms import UserCreateForm, UserLoginForm, UserResetPasswordForm
from email_task import send_user_register_email, send_forgot_password_email, send_reset_password_success_email
from django.contrib.auth import get_user_model
from accounts.models import UserAuthToken, UserForgetPassword
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
    template_name = "base.html"
    ctx = {}
    return render(request, template_name, ctx)

@login_required
def users_logout(request):
    logout(request)
    success_url = reverse_lazy("users-login")
    return redirect(success_url)


def users_login(request):
    template_name = "users/user_login.html"
    ctx = {}
    success_url = reverse_lazy("users-index")

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                login(request, user)
                return redirect(success_url)
            else:
                form.errors['username'] = ["Your username and password didn't match. Please try again."]
    else:
        form = UserLoginForm()

    ctx['form'] = form
    return render(request, template_name, ctx)


def users_forgot_password(request):
    template_name = "users/user_forgot_password.html"
    ctx = {}
    success_url = reverse_lazy("users-login")

    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if not UserForgetPassword.objects.filter(user=user).exists():
                forget_password_obj = UserForgetPassword.objects.create(token=UserAuthToken.generate_unique_key(), user=user)
            else:
                forget_password_obj = UserForgetPassword.objects.get(user=user)
            send_forgot_password_email(user, forget_password_obj.token)
            return redirect(success_url)
        else:
            ctx['error'] = 'Email does not exist ! Please enter Valid email'

    return render(request, template_name, ctx)


def users_reset_password(request, token):
    template_name = "users/user_reset_password.html"
    ctx = {}
    success_url = reverse_lazy("users-login")

    forget_password_obj = UserForgetPassword.objects.filter(token=token).first()
    if not forget_password_obj:
        return HttpResponse('Invalid link or link has been expired.')

    if request.method == 'POST':
        form = UserResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = forget_password_obj.user
            user.set_password(password)
            user.save()
            forget_password_obj.delete()
            send_reset_password_success_email(user)
            return redirect(success_url)
    else:
        form = UserResetPasswordForm()

    ctx['form'] = form
    return render(request, template_name, ctx)


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