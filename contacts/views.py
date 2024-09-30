from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages


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
        
        # 發送電郵
        send_mail(
            '聯絡表單提交',  # 主題
            f'姓名: {name}\n電郵: {email}\n電話: {phone}\n留言: {message}',  # 郵件內容
            'dpythonweb@gmail.com',  # 發件人
            ['dpythonweb@gmail.com'],  # 收件人
            fail_silently=False,
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




