from django.shortcuts import render, redirect
from .models import Bank
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your views here.
def bank(request):
    if request.method == 'POST':
        resident_id = request.POST['resident_id']
        resident_name = request.POST['resident_name']
        resident_code = request.POST['resident_code']
        payment_method = request.POST['payment_method']
        payment_month = request.POST['payment_month']
        payment_year = request.POST['payment_year']
        depositslip_photo = request.POST['depositslip_photo']
        message = request.POST['message']
        if request.user.is_authenticated:
            user_id = request.user.id
        has_banked = Bank.objects.all().filter(resident_id=resident_id, user_id=user_id)
        bank = Bank(resident_name=resident_name, resident_code=resident_code, payment_method=payment_method, payment_month=payment_month, payment_year=payment_year, message=message, depositslip_photo=depositslip_photo)
        bank.save()
        
        messages.success(request, '您的轉帳記錄已經上傳成功，如有進一步消息會盡快聯繫您!')        
        return redirect('dashboard')