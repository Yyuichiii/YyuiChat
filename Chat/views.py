from django.shortcuts import render,redirect
from .forms import UserRegisterForm,LoginForm
from django.contrib.auth import login,logout,authenticate,update_session_auth_hash
from django.contrib.auth.models import User
from .models import Chat,Message
from django.core.paginator import Paginator


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Fetch all users excluding the current user
    users = User.objects.exclude(pk=request.user.pk)

    context_list = []

    for user in users:
        # Filter chat where participants include both sender and receiver
        chat = Chat.objects.filter(participants=user).filter(participants=request.user).first()
        
        if chat:
            unread_msg_count = Message.objects.filter(chat=chat, is_read=False).count()
        else:
            unread_msg_count = 0

        context_list.append({
            'user': user,
            'count': unread_msg_count
        })

    print(context_list)
    return render(request, "Chat/home.html", {'users': users, 'context_list': context_list})


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

    # Get the receiver
    receiver = User.objects.get(pk=pk)

    # Filter chat where participants include both sender and receiver
    chat = Chat.objects.filter(participants=receiver).filter(participants=request.user).first()

    context = {}

    if chat:
        # Retrieve messages for the conversation
        messages = Message.objects.filter(chat=chat).order_by('-timestamp')

        # Mark unread messages as read
        unread_messages = messages.filter(is_read=False,sender=request.user)
        unread_messages.update(is_read=True)
        
        # Paginate the messages to fetch only the latest 10
        paginator = Paginator(messages, 6)
        page_number = request.GET.get('page')
        messages = paginator.get_page(page_number)
        context = {
        'messages': messages,
        
        }


    return render(request,"Chat/message.html",{'users':users,'receiver':receiver,'message':context})
