from django.shortcuts import render, HttpResponse, redirect
from app01 import models

from app01.utils.form import LoginForm
from app01.utils.code import check_code

from io import BytesIO


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功 获取到用户信息 form.cleaned_data
        # {'username': '123', 'password': 'cfdaf9256fd1262ab42bf8a3a573f338', 'code':'xxx'}
        # 需要校验
        # print(form.cleaned_data)

        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get("image_code", "")
        if code == "":
            form.add_error("code", "验证码已超时")
            return render(request, 'login.html', {"form": form})

        if user_input_code.upper() != code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {"form": form})

        # 去数据库校验用户和密码是否正确 获取用户对象
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:  # 如果 没查到 这位 None
            form.add_error("username", "用户名或密码错误")
            return render(request, 'login.html', {"form": form})

        # session cookie
        # 网站生成随机字符串 存到 cookie 中 浏览器 和服务器 各保存一份， info中 保存对应的session ，序列化到 django-session 表中
        # 检查-网络-全部-list-cookie sessionid 的随机字符串   django-session 表中
        # 不同浏览器 cookie session 不同
        request.session["info"] = {"id": admin_object.id, "username": admin_object.username}
        # session 可以保存一个月
        request.session.set_expiry(60 * 60 * 24 * 30)
        return redirect('/admin/list/')

    return render(request, 'login.html', {"form": form})


def logout(request):
    request.session.clear()
    return redirect("/login/")


def image_code(request):
    img, code_string = check_code()
    # print(code_string)

    # 写入到session中 （以便后续读取验证码 再进行校验）
    request.session['image_code'] = code_string
    # 给session设置60s的超时
    request.session.set_expiry(60)

    stream = BytesIO()  # 创建一个对象
    img.save(stream, 'png')  # 图片内容 写入内存

    return HttpResponse(stream.getvalue())
