from django.shortcuts import render, redirect
from .models import Booking
from django.contrib import messages
import re
from .choices import title_choices  # 引入你的 choices.py
from django.core.mail import send_mail

def information(request):
    context = {
        'title_choices': title_choices,  # 將 choices 傳遞到上下文中
        'errors': {},
    }

    if request.method == 'POST':
        title = request.POST.get('title', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        comment = request.POST.get('comment', '')
        visit_date = request.POST.get('visit_date', '')
        visit_time = request.POST.get('visit_time', '')

        # 驗證輸入數據
        errors = {}

        # 驗證名字
        if not name:
            errors['name'] = "姓名是必填的。"
        elif not re.match(r"^[\u4e00-\u9fa5a-zA-Z\s\-']+$", name):
            errors['name'] = "姓名只能包含中文字符、英文字母、空格、連字符和撇號。"
        
        # 驗證郵件
        if not email:
            errors['email'] = "電郵是必填的。"
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors['email'] = "請輸入有效的電郵地址。"

        # 驗證電話
        if not phone:
            errors['phone'] = "電話是必填的。"
        elif not re.match(r"^\d{8}$", phone):
            errors['phone'] = "請輸入有效的8位電話號碼。"

        # 驗證訪問日期和時間
        if not visit_date:
            errors['visit_date'] = "預約參觀日期是必填的。"
        if not visit_time:
            errors['visit_time'] = "預約參觀時間是必填的。"

        if errors:
            context.update({
                'errors': errors,
                'title': title,
                'name': name,
                'email': email,
                'phone': phone,
                'comment': comment,
                'visit_date': visit_date,
                'visit_time': visit_time,
            })
            messages.error(request, '您的信息提交不成功，請修改您的信息。')
            return render(request, 'informations/information.html', context)

        # 如果沒有錯誤，創建預約並保存
        booking = Booking(
            title=title,
            name=name,
            email=email,
            phone=phone,
            comment=comment,
            visit_date=visit_date,
            visit_time=visit_time
        )
        booking.save()
        
        email_subject = "預約表單提交"
        email_body = (
                        f'稱謂: {title}\n'
                        f'姓名: {name}\n'
                        f'電郵: {email}\n'
                        f'電話: {phone}\n'
                        f'預約參觀日期: {visit_date}\n'
                        f'預約參觀時間: {visit_time}\n'
                        f'留言: {comment}'
                        )

        # Send the email
        send_mail(
                    email_subject,
                    email_body,
                    "dpythonweb@gmail.com",
                    ['dpythonweb@gmail.com'],
                    fail_silently=False,
                    )
        
        # 顯示成功消息
        messages.success(request, '您的信息已成功提交，我們將盡快與您聯繫。')
        return redirect('information')

    return render(request, 'informations/information.html', context)

def guideline(request):
    return render(request, 'informations/guideline.html',)
