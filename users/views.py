from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def users_index(request):
    return HttpResponse("Test Users Index View.")


def user_create_view(request):
    template_name = "users/user_create.html"
    ctx = {}

    return render(request, template_name, ctx)