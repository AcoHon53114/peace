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
        
        # 創建 Contact 對象並保存到數據庫
        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
        
        # 顯示成功消息
        messages.success(request, '您的信息已成功提交，我們會盡快與您聯繫。')
        
        # 重定向到聯繫頁面
        return redirect('contact')
    
    return render(request, 'contacts/contact.html')