from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from residents.models import Resident
# Create your views here.

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        print(first_name)
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'登錄名稱已經存在')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'電郵地址已經存在')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username,
                                                password=password,
                                                email=email,
                                                first_name=first_name,
                                                last_name=last_name)
                    user.save()
                    messages.success(request, " : 您已經成功註冊和可以登錄!")
                    return redirect('login')
        else:
            messages.error(request,'密碼不正確!')
            print("密碼不正確!")
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, ' : 您已經成功登錄!')
            return redirect('dashboard')
        else:
            messages.error(request, '登錄失敗!Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, ' : 您已經成功登出!You are now logged out')
    return redirect('index')

def dashboard(request):
    user_contacts = Resident.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {'contacts': user_contacts}
    return render(request, 'accounts/dashboard.html', context)