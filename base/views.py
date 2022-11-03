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
def nearbyApi(request, pk=''):
    if request.method == 'GET':
        try:
            user = user_location.objects.get(userId=pk.split('&')[0])
            lat = user.latitude
            lng = user.longitude
            range = int(pk.split('&')[2])
            g = pk.split('&')[1]
            age = pk.split('&')[3]
            r = 0
            if range > 0 and range <=100:
                r = 3
            if range >=100 and range <= 1000:
                r = 2
            if range >=1000 and range <= 10000:
                r = 1
                           
            lat = lat.split('.')[0] + '.' + lat.split('.')[1][:r]
            lng = lng.split('.')[0] + '.' + lng.split('.')[1][:r]
            # return HttpResponse(lat+' '+lng+' '+ str(r)+' '+ age)
            location=user_location.objects.filter(latitude__startswith=lat,longitude__startswith=lng, gender=g, age__gte=age.split('-')[0], age__lte=age.split('-')[1])
            if location:
                location_seri=user_loacation_serializer(location,many=True)
                return JsonResponse(location_seri.data,safe=False)
            return JsonResponse('There is no one near you...', safe=False) 
        except Exception as e:
            return JsonResponse("Message : "+str(e),safe=False)       

        

        

        

            
       

        