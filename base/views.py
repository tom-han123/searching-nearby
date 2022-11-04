from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from . serializers import user_loacation_serializer
from . models import user_location
import json
import geopy.distance

def landing(request):
    return HttpResponse('Hello')

@csrf_exempt
def locationApi(request, pk=0):
    if request.method=='GET':
        try:
            if pk == 0:
                location=user_location.objects.all()
                location_seri=user_loacation_serializer(location,many=True)
            else:
                location=user_location.objects.get(userId=pk)
                location_seri=user_loacation_serializer(location,many=False)
            return JsonResponse(location_seri.data,safe=False)  
        except Exception as e:
            return JsonResponse("Message : "+str(e), safe=False)    
    elif request.method=='POST':
        location_data = JSONParser().parse(request)
        location_seri = user_loacation_serializer(data=location_data)
        if location_seri.is_valid():
            location_seri.save()
            return JsonResponse('Added Successfully...',safe=False)
        return JsonResponse('failed to add',safe=False)  
    elif request.method=='PUT':
        try:
            location_data = JSONParser().parse(request)
            single_location= user_location.objects.get(userId=pk)
            location_seri = user_loacation_serializer(single_location,data=location_data)
            if location_seri.is_valid():
                location_seri.save()
                return JsonResponse('update successfully',safe=False)
            return JsonResponse('failed to update',safe=False)
        except Exception as e:
            return JsonResponse("Message : "+str(e), safe=False)     
    elif request.method=='DELETE':
        try:
            singleloc = user_location.objects.get(userId=pk)
            singleloc.delete()
            return JsonResponse('Delete Successfully...',safe=False)
        except Exception as e:
            return JsonResponse("Message : "+str(e), safe=False)    

@csrf_exempt
def nearbyApi(request, pk='', rng='', gen='', age=''):
    if request.method == 'GET':
        try:
            user = user_location.objects.get(userId=pk)
            lat = user.latitude
            lng = user.longitude
            coor1 = (lat,lng)
            range = int(rng)       
            lat = lat.split('.')[0] + '.' + lat.split('.')[1][:1]
            lng = lng.split('.')[0] + '.' + lng.split('.')[1][:1]
            # return HttpResponse(lat+' '+lng+' '+ str(r)+' '+ age)
            location_list = user_location.objects.filter(latitude__startswith=lat,longitude__startswith=lng).values()
            user_li = []
            for person in location_list:
                coor2 = (list(person.values())[7],list(person.values())[8])
                distance = geopy.distance.geodesic(coor1, coor2).m
                print(distance)
                if distance <= range:
                    user_li.append(list(person.values())[1])
            if user_li:
                location=user_location.objects.filter(userId__in = user_li, gender=gen, age__gte=age.split('-')[0], age__lte=age.split('-')[1])
                location_seri=user_loacation_serializer(location,many=True)
                return JsonResponse(location_seri.data,safe=False)
            return JsonResponse('There is no one near you...', safe=False) 
        except Exception as e:
            return JsonResponse("Message : "+str(e),safe=False)       

        

        

        

            
       

        