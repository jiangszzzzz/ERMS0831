from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModleForm, PrettyNumModleForm, PrettyNumEidtModleForm


def user_list(request):
    queryset = models.User_info.objects.all()

    page_object = Pagination(request, queryset, page_size=2)
    context = {
        "queryset": page_object.page_queryset,  # 分完页之后的数据
        "page_string": page_object.html()  # 页面中的页码
    }

    return render(request, "user_list.html", context)


# ##################################  modleForm 实现   ##################################


def user_add(request):
    # if request.method == "GET":
    #     context = {
    #         "gender_choices": models.User_info.gender_choices,
    #         "depart_list": models.Department.objects.all(),
    #     }
    #     return render(request, "user_add.html", context)

    # 获取数据(原始方法)
    # user = request.POST.get("name")......
    # models.User_info.objects.create(name = user)

    if request.method == "GET":
        form = UserModleForm()
        return render(request, "user_add.html", {"form": form})

    # POST 提交数据校验
    form = UserModleForm(data=request.POST)
    # 添加校验
    if form.is_valid():
        # 存储到表里面
        form.save()
        return redirect("/user/list")

    return render(request, "user_add.html", {"form": form})


def user_edit(request, nid):
    """修改部门"""
    # http://127.0.0.1:8000/user/1/edit/
    row_object = models.User_info.objects.filter(id=nid).first()

    if request.method == "GET":
        form = UserModleForm(instance=row_object)
        return render(request, "user_edit.html", {"form": form})

    form = UserModleForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存 用户输入的所有数据， 如果想保存用户输入以外增加一点值
        # form.instance.password（字段名） = 值

        form.save()  # 添加数据
        return redirect("/user/list")
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    """删除部门"""
    # http://127.0.0.1:8000/depart/delete/?nid=1
    # nid = request.GET.get('nid')
    models.User_info.objects.filter(id=nid).delete()
    return redirect("/user/list/")
