from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from login.settings import BASE_DIR
# Create your views here.
import os
def home(request):
    return render(request,"authentication/index.html")

def signup(request):
    # list content ->> [username,fname,lname,email,pass1,pass2]
    if request.method == "POST":
        key = ['username','Firstname','Lastname','email','password','password']
        values = [request.POST[x] for x in key]
        itr = 0
        for i in values:
            if not i:
                messages.error(request,"{} field cannot be empty".format(key[itr]))
                return redirect('home')
            itr+=1
        
        if User.objects.filter(username=values[0]):
            messages.error(request,"Username Already exists. Please try a different username!")
            return redirect('home')
        
        if User.objects.filter(email=values[3]):
            messages.error(request,"Email is already registered. Please use a different email!")
            return redirect('home')
        
        if len(values[0])>10:
            messages.error(request,"Username must be under 10 characters!")
            return redirect('home')
        
        if len(values[4])<=4:
            messages.error(request,"Passwords must be atleast 5 characters!")
            return redirect('home')
        
        if values[4]!=values[5]:
            messages.error(request,"Entered Passwords do not match!")
            return redirect('home')
            
        if not values[0].isalnum():
            messages.error(request,"Username must be Alphanumeric")
            return redirect('home')
        
        myuser = User.objects.create_user(values[0],values[3],values[4])
        myuser.first_name = values[1]
        myuser.last_name = values[2]
        myuser.save()
        messages.success(request,"Your Account has been successfully Created")
        return redirect('signin')
    return render(request,"authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        user = authenticate(username=username,password=pass1)
        name = user.first_name
        if user is not None:
            login(request,user)
            return render(request,'authentication/index.html',{'fname':name})
        else:
            messages.error(request,"Bad Credentials")
            redirect('home')
    return render(request,"authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('home')

def show_user(request):
    allusers = User.objects.all()
    render(request,os.path.join(BASE_DIR,"\\templates\\index.html"),{'users':allusers})
    
