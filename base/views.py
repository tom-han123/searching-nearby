from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from . serializers import user_loacation_serializer
from . models import user_location
import json

def landing(request):
    return HttpResponse('Hello')

@csrf_exempt
def locationApi(request, pk=0, lpk=0):
    if request.method=='GET':
        try:
            if pk == 0:
                location=user_location.objects.all()
                location_seri=user_loacation_serializer(location,many=True)
            else:
                location=user_location.objects.get(userId=pk)
                location_seri=user_loacation_serializer(location,many=False)
            return JsonResponse(location_seri.data,safe=False)
        except Exception:
            return HttpResponse('User does not exit...')
    elif request.method=='POST':
        location_data = JSONParser().parse(request)
        location_seri = user_loacation_serializer(data=location_data)
        if location_seri.is_valid():
            location_seri.save()
            return JsonResponse('Added Successfully...',safe=False)
        return JsonResponse('failed to add',safe=False)    
    elif request.method=='PUT':
        location_data = JSONParser().parse(request)
        single_location= user_location.objects.get(locationId=pk)
        location_seri = user_loacation_serializer(single_location,data=location_data)
        if location_seri.is_valid():
            location_seri.save()
            return JsonResponse('update successfully',safe=False)
        return JsonResponse('failed to update',safe=False)
    elif request.method=='DELETE':
        singleloc = user_location.objects.get(locationId=lpk)
        singleloc.delete()
        return JsonResponse('Delete Successfully...',safe=False)

@csrf_exempt
def nearbyApi(request, loc=''):
    if request.method == 'GET':
        lat =loc.split('&')[0]
        lng =loc.split('&')[1]
        range = loc.split('&')[2]
        g = loc.split('&')[3]
        if len(range) <=3 :
            r = 3
        elif len(range) == 4:
            r = 2
        elif len(range) == 5:
            r = 1
        else:
            r = 0    
        lat = lat.split('.')[0] + '.' + lat.split('.')[1][:r]
        lng = lng.split('.')[0] + '.' + lng.split('.')[1][:r]
        location=user_location.objects.filter(latitude__startswith=lat,longitude__startswith=lng, gender=g)
        if location:
            location_seri=user_loacation_serializer(location,many=True)
            return JsonResponse(location_seri.data,safe=False)
        return JsonResponse('There is no one near you...', safe=False)    

        

        

            
       

        