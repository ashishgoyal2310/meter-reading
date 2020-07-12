import json 
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from accounts.models import UserAuthToken
from accounts.utils import api_authentication
from django.http import HttpResponse, JsonResponse
from meters.models import UserMeter, MeterHealth

# Create your views here.

@csrf_exempt
@api_authentication
def register(request):
    user = request.user
    data = json.loads(request.body)
    print(data)
    if request.method == "POST":
        # import pdb; pdb.set_trace()
        meter_number = data.get('meter_number')
        address = data.get('address')
        state = data.get('state')
        zipcode = data.get('zipcode')
        location = data.get('location')
        siteid = data.get('siteid')
        configurations = data.get('configurations')
        warranty = data.get('warranty')
        model_type = data.get('model_type')

        if len(str(meter_number))<=7 or len(zipcode)!=6:
            response = {
                'meter_number':meter_number if len(str(meter_number))>=8 else 'Meter Number should be greater than or equals to 8',
                'address': address if address else 'Field Required',
                'state': state if state else 'Field Required',
                'zipcode': zipcode if len(zipcode)==6 else 'Zip Code should be of 6 length only',
            }
            return JsonResponse(response, safe=True, status=400)
        else:
            kwargs = {'user':request.user,'meter_number':meter_number,'address': address, 'state': state, 'zipcode': zipcode, 'location':location,'siteid':siteid,'configurations':configurations,'warranty':warranty,'model_type':model_type}
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
                'location':location,
                'siteid':siteid,
                'configurations':configurations,
                'warranty':warranty,
                'model_type':model_type
            }
            return JsonResponse(response, safe=True, status=200)

    
    else:
        return JsonResponse({}, safe=True, status=405)


@csrf_exempt
@api_authentication
def all_meters(request):
    if request.method == 'POST':
        # all_meter_obj = UserMeter.objects.filter(user=request.user)
        all_meter_obj = UserMeter.objects.select_related('user').filter(user=request.user)
        new_response=[]
        for amo in all_meter_obj:
            response = {
                    'id': amo.id,
                    'user':amo.user.username,
                    'meter_number':amo.meter_number,
                    'address': amo.address,
                    'state': amo.state,
                    'zipcode': amo.zipcode,
                }
            new_response.append(response)
        return JsonResponse(new_response, safe=False, status=200)
            
    
@csrf_exempt
@api_authentication
def info(request,pid):
    if request.method == 'GET':
        try:
            meter_obj = UserMeter.objects.get(id=pid,user=request.user)
        except Exception as e:
            response = {'msg':"No Match found"}
            return JsonResponse(response, safe=True, status=400)
        
        response = {
                        'id': meter_obj.id,
                        'user':meter_obj.user.username,
                        'meter_number':meter_obj.meter_number,
                        'address': meter_obj.address,
                        'state': meter_obj.state,
                        'zipcode': meter_obj.zipcode,
                    }
        return JsonResponse(response, safe=True, status=200)

    elif request.method == 'DELETE':
        try:
            meter_obj = UserMeter.objects.get(id=pid,user=request.user)
            meter_num = meter_obj.meter_number
        except Exception as e:
            return HttpResponse("No match found")
        meter_obj.delete()
        return HttpResponse("Meter {} information deleted".format(meter_num))

    elif request.method == 'PUT':
        try:
            meter_obj = UserMeter.objects.get(id=pid,user=request.user)
            meter_num = meter_obj.meter_number
            new_address = json.loads(request.body)
            if 'address' not in new_address or not new_address['address']:
                return HttpResponse("No address key found")
        except Exception as e:
            return HttpResponse("No match found PUT method")
        # import pdb;pdb.set_trace()
        meter_obj.address = new_address.get('address')
        meter_obj.save()
        return HttpResponse("Meter {} address updated as {}".format(meter_num,meter_obj.address))


@csrf_exempt
@api_authentication
def reading(request,pid):
    if request.method == 'POST':
        # import pdb; pdb.set_trace()
        try:
            meter_obj = UserMeter.objects.get(id=pid,user=request.user)
        except Exception as e:
            response = {'msg':"No data Found"}
            return JsonResponse(response, safe=True, status=400)
        data = json.loads(request.body)
        meter_status = data.get('meter status')
        meter_reading = data.get('meter reading')
        reading_date = data.get('reading date')

        MeterHealth.objects.create(user_meter=meter_obj,meter_status=meter_status,meter_reading=meter_reading,reading_date=reading_date)
        response = {
                        'id': meter_obj.id,
                        'user':meter_obj.user.username,
                        'meter_number':meter_obj.meter_number,
                        'meter_status': meter_status,
                        'meter_reading': meter_reading,
                        'reading_date': reading_date
                    }
        return JsonResponse(response, safe=True, status=200)


@csrf_exempt
@api_authentication
def status_info(request):
    print(request.user.id)
    if request.method == 'GET':
        param_meter_number = request.GET.get('meter_number','')
        health_objs_qs = MeterHealth.objects.filter(user_meter__user_id=request.user.id)
        if param_meter_number != '': 
            health_objs_qs = health_objs_qs.filter(user_meter__meter_number=param_meter_number)

        new_response=[]
        for obj in health_objs_qs:
            response = {
                        'id': obj.id,
                        'meter_number':obj.user_meter.meter_number,
                        'username':obj.user_meter.user.username,
                        'meter_status':obj.meter_status,
                        'meter_reading': obj.meter_reading
                        }
            new_response.append(response)
        return JsonResponse(new_response, safe=False, status=200)

