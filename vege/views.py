from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
def rece(request):
    if request.method =="POST":
        data=request.POST#to get our data from front to here we have to do this method
        receipe_image=request.FILES.get('receipe_image')#for files we have different request format 
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')
    #   print(receipe_name)
    #   print(receipe_description)
    #   print(receipe_image)
    # to save data in model 
        Receipe.objects.create(
          receipe_image=receipe_image,
          receipe_name=receipe_name,
          receipe_description=receipe_description, 
          )
        return redirect('/rece/')
    queryset=Receipe.objects.all()
    context={'Receipe': queryset}
    return render(request , 'rece.html',context)

def delf(request,id):
    queryset=Receipe.objects.get(id=id)
    queryset.delete()
    return render(request , 'rece.html')

def updf(request,id):
    queryset=Receipe.objects.get(id=id)
    
    if request.method=="POST":
        data=request.POST#to get our data from front to here we have to do this method
        receipe_image=request.FILES.get('receipe_image')#for files we have different request format 
        receipe_name=data.get('receipe_name')
        receipe_description=data.get('receipe_description')
        
        queryset.receipe_image=receipe_image
        queryset.receipe_name=receipe_name
        
        if receipe_image:
         queryset.receipe_description=receipe_description
         
        queryset.save() 
        return redirect('/rece/')
        
    context={'Receipe':queryset}
    
    return render(request,'Updf_vege.html',context)
def login(request):
    return render(request,'login.html')
def register(request):
     if request.method =="POST":
         first_name=request.POST.get('first_name')
         last_name=request.POST.get('last_name')
         username=request.POST.get('username')
         password=request.POST.get('password')
         
         user=User.objects.filter(username=username)
         if user.exists():
            messages.info(request, "Username already taken")
            return redirect('/register/') 
         user=User.objects.create(
             first_name=first_name,
             last_name=last_name,
             username=username,
            #  password=password #this method will not work because password should be encrypted 
         )
        #  therefore this 
         user.set_password(password)
         user.save()
         return redirect('/register/')

         
     return render(request,'register.html')