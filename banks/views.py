# /Users/minkeihon/Desktop/peace/banks/views.py
from django.shortcuts import render, redirect
from .models import Bank
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse
from django.conf import settings

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
        
        # Format uploaded_date
        uploaded_date = bank.uploaded_date.strftime('%Y年%m月%d日 %I:%M %p')
        
        # Generate admin change URL
        admin_change_url = request.build_absolute_uri(reverse('admin:banks_bank_change', args=[bank.id]))
        
        # Generate image URL
        image_url = request.build_absolute_uri(settings.MEDIA_URL + str(bank.depositslip_photo))
        
        email_subject = "上傳轉帳記錄表單提交"
        email_body = (
                        f'院友編號: {resident_code}<br>'
                        f'院友姓名: {resident_name}<br>'
                        f'付款方式: {payment_method}<br>'
                        f'付款年份: {payment_year}<br>'
                        f'付款月份: {payment_month}<br>'
                        f'轉帳記錄: <a href="{image_url}">點擊這裡查看上傳附件</a><br>'
                        f'備註/留言: {message}<br>'
                        f'上傳日期和時間: {uploaded_date}<br>'
                        f'查看記錄: <a href="{admin_change_url}">點擊這裡</a><br>'
                        )

        # Send the email
        send_mail(
                    email_subject,
                    email_body,
                    "dpythonweb@gmail.com",
                    ['dpythonweb@gmail.com'],
                    fail_silently=False,
                    html_message=email_body,  # Use html_message for HTML content
                    )
        
        messages.success(request, '您的轉帳記錄已經上傳成功，如有進一步消息會盡快聯繫您!')        
        return redirect('dashboard')
    else:
        # Handle GET request or other methods
        return render(request, 'bank.html')