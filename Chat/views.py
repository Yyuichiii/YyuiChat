from django.shortcuts import render,redirect
from .forms import UserRegisterForm,LoginForm
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.contrib.auth.models import User

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Fetch all users excluding the current user
    users = User.objects.exclude(pk=request.user.pk)
    
    return render(request,"Chat/home.html",{'users':users})


def login_view(request):
    
    fm = LoginForm()
    if request.method == 'POST':
        fm = LoginForm(request.POST)
        
        if fm.is_valid():
            
            username=fm.cleaned_data['username'] 
            upas=fm.cleaned_data['password']
            
            user = authenticate(username=username,password=upas)
            if user is not None:
                login(request,user)                               
                return redirect('home') 



    return render(request,"Chat/login.html",{'form':fm})

def register(request):
    if request.method=='POST':
        fm=UserRegisterForm(request.POST)
        
        if fm.is_valid():
            fm.save()
            
            return redirect('login')
        return render(request,"Chat/register.html",{'form':fm})

    else:
        fm=UserRegisterForm()
        return render(request,"Chat/register.html",{'form':fm})


def logout_view(request):
    logout(request)
    return redirect('login')


def message_view(request,pk):
    # Fetch all users excluding the current user
    users = User.objects.exclude(pk=request.user.pk)
    receiver=User.objects.get(pk=pk)
    return render(request,"Chat/message.html",{'users':users,'receiver':receiver})
