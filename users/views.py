from django.shortcuts import render
from django.http import HttpResponse

from users.forms import UserCreateForm
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def users_index(request):
    return HttpResponse("Test Users Index View.")


def user_list_view(request):
    template_name = "users/user_list.html"
    all_users = User.objects.all()
    print(all_users)
    ctx = {'all_users': all_users}
    return render(request, template_name, ctx)


def user_create_view(request):
    template_name = "users/user_create.html"
    ctx = {}
    RANDOM_PWD = '123456'

    if request.method == 'POST':
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(RANDOM_PWD)
            user.save()
            form = UserCreateForm()
            ctx['message'] = "User '{}' created successfully.".format(user.username)
    else:
        form = UserCreateForm()

    ctx['form'] = form
    return render(request, template_name, ctx)