# /Users/minkeihon/Desktop/peace/banks/views.py
from django.shortcuts import render, redirect
from .models import Bank
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
import datetime

# Create your views here.
def bank(request):
    if request.method == 'POST':
        resident_id = request.POST['resident_id']
        resident_name = request.POST['resident_name']
        resident_code = request.POST['resident_code']
        payment_method = request.POST['payment_method']
        payment_month = request.POST['payment_month']
        payment_year = request.POST['payment_year']
        depositslip_photo = request.FILES['depositslip_photo']  # Use request.FILES for file uploads
        message = request.POST['message']
        
        # Ensure user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, '用户未登录。')
            return redirect('dashboard')
        
        user_id = request.user.id
        
        has_banked = Bank.objects.filter(resident_id=resident_id, user_id=user_id)
        
        bank = Bank(
            user_id=user_id,
            resident_id=resident_id,
            resident_name=resident_name,
            resident_code=resident_code,
            payment_method=payment_method,
            payment_month=payment_month,
            payment_year=payment_year,
            depositslip_photo=depositslip_photo,
            message=message
        )
        bank.save()
        
        email_subject = "上傳轉帳記錄表單提交"
        email_body = (
                        f'院友編號: {resident_code}\n'
                        f'院友姓名: {resident_name}\n'
                        f'付款方式: {payment_method}\n'
                        f'付款年份: {payment_year}\n'
                        f'付款月份: {payment_month}\n'
                        f'轉帳記錄: {depositslip_photo}\n'
                        f'備註/留言: {message}'
                        )

        # Send the email
        send_mail(
                    email_subject,
                    email_body,
                    "dpythonweb@gmail.com",
                    ['dpythonweb@gmail.com'],
                    fail_silently=False,
                    )
        
        messages.success(request, '您的轉帳記錄已經上傳成功，如有進一步消息會盡快聯繫您!')        
        return redirect('dashboard')
    else:
        # Handle GET request or other methods
        return render(request, 'bank.html')
'''
def dashboard(request):
    user_banks = Bank.objects.filter(user_id=user_id).order_by('-uploaded_date')[:6]  # Get the latest 6 records
    context = {'banks': user_banks}
    return render(request,'accounts/dashboard.html', context)
'''
'''
def dashboard(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        records = Bank.objects.filter(user_id=user_id).order_by('-uploaded_date')[:6]  # Get the latest 6 records
        return render(request, 'accounts/dashboard.html', {'records': records})
    else:
        messages.error(request, '用户未登录。')
        return redirect('login')
'''