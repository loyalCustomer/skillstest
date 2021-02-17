from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,HTTP_204_NO_CONTENT
from rest_framework.generics import RetrieveAPIView

from .serializers import UserSerializer

@api_view(['GET','POST'])
def getUsers(request):
    if request.method == 'GET':
        myusers=User.objects.all()
        serializer = UserSerializer(myusers, many=True)
        return Response (serializer.data) 
    
    if request.method == 'POST':
        first_name = ''
        last_name = ''

        if 'first_name' in request.data:
            first_name = request.data["first_name"]
        if 'last_name' in request.data:
            last_name = request.data["last_name"]
          
        #last_name = request.data["last_name"]
        #query_dict = request.data
        #my_dict={}
        #my_dict = query_dict.lists()
        mypass=request.data['password']
        myword = make_password(mypass)
        myuser=request.data['username']
        serializer = UserSerializer(data={'username':myuser,'password':myword, 'first_name':first_name,'last_name':last_name})
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=HTTP_201_CREATED)
        else:
            return Response (serializer.errors, status=HTTP_400_BAD_REQUEST) 


@api_view(['GET','PUT','PATCH','DELETE'])
def getUser(request,pk):
    requested_user = User.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = UserSerializer(requested_user)
        return Response (serializer.data)
    elif request.method == 'PUT' or request.method =='PATCH':
        first_name = ''
        last_name = ''

        if 'first_name' in request.data:
            first_name = request.data["first_name"]
        if 'last_name' in request.data:
            last_name = request.data["last_name"]
        mypass=request.data['password']
        myword = make_password(mypass)
        myuser=request.data['username']
        serializer = UserSerializer(requested_user,data={'username':myuser,'password':myword, 'first_name':first_name,'last_name':last_name})
        #serializer = UserSerializer(requested_user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data)
        return Response (serializer.errors, status=HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        requested_user.delete()
        return Response(status=HTTP_204_NO_CONTENT)
#class UserDetailsView (RetrieveAPIView):
  #  queryset = User.objects.all()
 #   serializer_class = UserSerializer
    
