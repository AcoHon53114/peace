from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from datetime import datetime
from django.urls import reverse
from django.conf import settings

# Create your views here.

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        # 顯示成功消息
        messages.success(request, '您的信息已成功提交，我們會盡快與您聯繫。')
        
        # 創建 Contact 對象並保存到數據庫
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
        
        # Format contact_date
        contact_date = contact.contact_date.strftime('%Y年%m月%d日 %I:%M %p')
        
        # Generate admin change URL
        admin_change_url = request.build_absolute_uri(reverse('admin:contacts_contact_change', args=[contact.id]))
        
        # 發送電郵
        send_mail(
            '聯絡表單提交',  # 主題
            f'姓名: {name}\n電郵: {email}\n電話: {phone}\n留言: {message}\n傳送日期和時間: {contact_date}\n查看記錄: 點擊這裡',  # 純文本內容
            'dpythonweb@gmail.com',  # 發件人
            ['dpythonweb@gmail.com'],  # 收件人
            fail_silently=False,
            html_message=f'姓名: {name}<br>電郵: {email}<br>電話: {phone}<br>留言: {message}<br>傳送日期和時間: {contact_date}<br>查看記錄: <a href="{admin_change_url}">點擊這裡</a>'  # HTML 內容
        )
    return render(request, 'contacts/contact.html')

def contact_view(request):
    if request.method == 'POST':
        # 假設你在這裡處理表單數據
        # 例如：form = ContactForm(request.POST)
        
        # 設置成功消息
        messages.success(request, '您的信息已成功提交，我們會盡快與您聯繫。')
    
        # 重定向到聯繫頁面
        return redirect('contact')
    
    return render(request, 'contacts/contact.html')