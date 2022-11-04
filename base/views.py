from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from . serializers import user_loacation_serializer
from . models import user_location
import geopy.distance
import geocoder

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
            user = user_location.objects.get(userId=pk)
            lat = user.latitude
            lng = user.longitude
            coor1 = (lat,lng)   
            lat = lat.split('.')[0] + '.' + lat.split('.')[1][:1]
            lng = lng.split('.')[0] + '.' + lng.split('.')[1][:1]

            range = int(request.GET.get('range'))
            gen = request.GET.get('gender')
            age = str(request.GET.get('age'))

            location_list = user_location.objects.filter(latitude__startswith=lat,longitude__startswith=lng).values()
            user_li = []

            for person in location_list:
                coor2 = (list(person.values())[7],list(person.values())[8])
                distance = geopy.distance.geodesic(coor1, coor2).m
                print(distance)
                if distance <= range:
                    user_li.append(list(person.values())[1])

            if user_li:
                if gen == '':
                    if age == '':
                        location=user_location.objects.filter(userId__in = user_li)
                    elif '-' in age:
                        location=user_location.objects.filter(userId__in = user_li, age__gte=age.split('-')[0], age__lte=age.split('-')[1])
                    elif 'lt' in age:
                        location=user_location.objects.filter(userId__in = user_li, age__lt=age[2:])        
                    elif 'gt' in age:
                        location=user_location.objects.filter(userId__in = user_li, age__gt=age[2:])
                    else:
                        location=user_location.objects.filter(userId__in = user_li, age=age)
                else:
                    if age == '':
                        location=user_location.objects.filter(userId__in = user_li, gender=gen)
                    elif '-' in age:
                        location=user_location.objects.filter(userId__in = user_li, gender=gen, age__gte=age.split('-')[0], age__lte=age.split('-')[1])
                    elif 'lt' in age:
                        location=user_location.objects.filter(userId__in = user_li, gender=gen, age__lt=age[2:])        
                    elif 'gt' in age:
                        location=user_location.objects.filter(userId__in = user_li, gender=gen, age__gt=age[2:])
                    else:
                        location=user_location.objects.filter(userId__in = user_li, gender=gen, age=age)        
                location_seri=user_loacation_serializer(location,many=True)
                return JsonResponse(location_seri.data,safe=False)
            return JsonResponse('There is no one near you...', safe=False) 
        except Exception as e:
            return JsonResponse("Message : "+str(e),safe=False)       
@csrf_exempt
def search_nearby(request):
    context ={}
    return render(request, 'base/front_end.html')
        

            
       

        