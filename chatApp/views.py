from django.shortcuts import render , redirect
from .models import User
from django.contrib.auth import authenticate , login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .schema import schema
import re
# Create your views here.
def lobby(request):
    return render(request , 'chat/main.html')
def register(request):
    if request.method =="GET":
        return render(request, "chat/register.html")
    if request.method == "POST":
        try : 
            username=request.POST.get("username")
            Email = request.POST.get("email")
            password = request.POST.get("password")
            # 3jazt nkhmam f regex tbh 
            if len(password)<8:
                return render(request, "chat/register.html",context={"Error":"password should be minimum 8 carecters"})
            user = User.objects.create_user(username=username , password=password , email = Email)
            user.save()
            return render(request, "chat/login.html")
        except Exception as e:
            print(e)
            return render(request, "chat/register.html",context={"Error":"Error occured try change the username or email"})
def loging(request):
    if request.method == "GET":
        return render(request, "chat/login.html")
    if request.method =="POST":
        username=request.POST.get("username")
        password = request.POST.get("password")
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            user = User.objects.get(username=username)
            rooms = room.objects.filter(user = user)
            response =render(request, "chat/home.html" ,context={"rooms":rooms})
            response.set_cookie('username', username, max_age=360000)
            return response
        else :
            return render(request, "chat/login.html",context={"Error":"you can't login with this credentials"})
        
@login_required(login_url='/login/')
def home(request):
    if request.method == "GET":
        username = request.COOKIES.get("username")
        user = User.objects.get(username=username)
        rooms = room.objects.filter(user = user)
        return render(request , "chat/home.html" , context={"rooms":rooms} )
        
    if request.method =="POST":
        room_name = request.POST.get("room_name")
        username = request.COOKIES.get("username")
        user = User.objects.get(username=username)
        rooms = room.objects.filter(user=user , room_name=room_name)
        if len(rooms)==0 :
            new_room = room.objects.create(user=user , room_name=room_name)
            new_room.save()
        messages = message.objects.filter(chat_room = room_name).order_by('date')
        return render(request , 'chat/main.html' , context={"room":room_name ,"messages":messages})

@login_required(login_url='/login/')
def chat_by_room(request , pk):
    messages = message.objects.filter(chat_room = pk).order_by('date')
    return render(request , 'chat/main.html' , context={"room":pk , "messages":messages})

@login_required(login_url='/login/')
def profile(request , pk):
    # get only the data needed with this query : 
    query = """
        query($username: String!) {
            profileData(username: $username) {
                id
                user {
                    username
                    email
                }
                description
                joinedUs
                specilality
            }
        }
    """
    data = schema.execute(query , variables={'username': pk},context=request )
    print(data.data.get("profileData"))
    return render(request , "chat/profile.html" , context=data.data.get("profileData")[0])