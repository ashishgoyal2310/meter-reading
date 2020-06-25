import json 
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from accounts.models import UserAuthToken
from accounts.utils import api_authentication
from django.http import HttpResponse, JsonResponse
from meters.models import UserMeter

# Create your views here.

@csrf_exempt
@api_authentication
def register(request):
    user = request.user
    if request.method == "POST":
        meter_number = request.POST.get('meter_number')
        address = request.POST.get('address')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        if len(meter_number)<=7 or len(zipcode)!=6:
            response = {
                'meter_number':meter_number if len(meter_number)>=8 else 'Meter Number should be greater than or equals to 8',
                'address': address if address else 'Field Required',
                'state': state if state else 'Field Required',
                'zipcode': zipcode if len(zipcode)==6 else 'Zip Code should be of 6 length only',
            }
            return JsonResponse(response, safe=True, status=400)
        else:
            kwargs = {'user':request.user,'meter_number':meter_number,'address': address, 'state': state, 'zipcode': zipcode}
            if UserMeter.objects.filter(meter_number=meter_number).exists():
                userm = UserMeter.objects.get(meter_number=meter_number)
                response = {'status': False, 'error':'Meter already exists with %s' %(userm.user)}
                return JsonResponse(response, safe=True, status=400)
            total_count = UserMeter.objects.filter(user=request.user).count()
            if total_count>=5:
                response = {'status': False, 'error':'You cannot register more than 5 meters'}
                return JsonResponse(response, safe=True, status=400)
            user_meter_obj = UserMeter.objects.create(**kwargs)
            response = {
                'user':request.user.username,
                'meter_number':meter_number,
                'address': address,
                'state': state,
                'zipcode': zipcode,
            }
            return JsonResponse(response, safe=True, status=200)

    
    else:
        return JsonResponse({}, safe=True, status=405)
