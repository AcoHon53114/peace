from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from residents.models import Resident
from banks.choices import payment_method_choices, payment_month_choices, payment_year_choices
from datetime import datetime

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        resident_name = request.POST['resident_name']
        resident_code = request.POST['resident_code']
        resident_description = request.POST['resident_description']
        resident_contact_person = request.POST['resident_contact_person']
        resident_contact_phone = request.POST['resident_contact_phone']
        resident_contact_email = request.POST['resident_contact_email']
        resident_contact_relation = request.POST['resident_contact_relation']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, '登錄名稱已經存在')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, '電郵地址已經存在')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username,
                                                    password=password,
                                                    email=email,
                                                    first_name=first_name,
                                                    last_name=last_name)
                    user.save()

                    # 創建 Resident 實例
                    resident = Resident(
                        username=user,
                        resident_name=resident_name,
                        resident_code=resident_code,
                        resident_description=resident_description,
                        resident_contact_person=resident_contact_person,
                        resident_contact_phone=resident_contact_phone,
                        resident_contact_email=resident_contact_email,
                        resident_contact_relation=resident_contact_relation,
                    )
                    resident.save()

                    messages.success(request, ": 您已經成功註冊和可以登錄!")
                    return redirect('login')
        else:
            messages.error(request, '密碼不正確!')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, ': 您已經成功登錄!')
            return redirect('dashboard')
        else:
            messages.error(request, '登錄失敗!')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, ': 您已經成功登出!')
    return redirect('index')

def dashboard(request):
    context = {
        'payment_method_choices': payment_method_choices.items(),
        'payment_month_choices': payment_month_choices.items(),
        'payment_year_choices': payment_year_choices.items(),
    }
    return render(request, 'accounts/dashboard.html', context)