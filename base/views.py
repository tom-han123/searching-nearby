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
            
            #extract user_list by filtering with latitude & longitude points range within 10km
            location_list = user_location.objects.filter(latitude__startswith=lat,longitude__startswith=lng).values()

            range = int(request.GET.get('range'))
            gen = request.GET.get('gender')
            age = str(request.GET.get('age'))

            #filter new_user_li by age range and gender
            user_li = []
            for person in location_list:
                coor2 = (list(person.values())[7],list(person.values())[8])
                distance = geopy.distance.geodesic(coor1, coor2).m
                print(distance)
                if distance <= range:
                    if gen == '':
                        if age == '':
                            user_li.append(dict(person))
                        elif '-' in age:
                            if int(list(person.values())[6]) >= int(age.split('-')[0]) and  int(list(person.values())[6]) <= int(age.split('-')[1]):
                                user_li.append(dict(person))  
                        elif 'gte' in age:
                            if int(list(person.values())[6]) >= int(age[3:]):
                                user_li.append(dict(person))
                        elif 'lte' in age:
                            if int(list(person.values())[6]) <= int(age[3:]):
                                user_li.append(dict(person))
                    else:
                        if age == '':
                            if list(person.values())[5] == gen:
                                user_li.append(dict(person))
                        elif  '-' in age:
                            if int(list(person.values())[6]) >= int(age.split('-')[0]) and  int(list(person.values())[6]) <= int(age.split('-')[1]) and list(person.values())[5] == gen:
                                user_li.append(dict(person))           
                        elif 'gte' in age:
                            if int(list(person.values())[6]) >= int(age[3:]) and list(person.values())[5] == gen: 
                                user_li.append(dict(person))
                        elif 'lte' in age:
                            if int(list(person.values())[6]) <= int(age[3:]) and list(person.values())[5] == gen:
                                user_li.append(dict(person))
                        else:
                            if int(list(person.values())[6]) == int(age) and list(person.values())[5] == gen:
                                user_li.append(dict(person))                 
            if user_li:
                return JsonResponse(user_li, safe=False)
            return JsonResponse('There is no one near you...', safe=False) 
        except Exception as e:
            return JsonResponse("Message : "+str(e),safe=False)       
@csrf_exempt
def search_nearby(request):
    context ={}
    return render(request, 'base/front_end.html')
        

            
       

        