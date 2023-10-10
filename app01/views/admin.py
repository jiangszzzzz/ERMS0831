from django.shortcuts import render, redirect

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import AdminModelForm


def admin_list(request):
    # 管理员

    # 构造搜索条件
    data_dict = {}
    search_data = request.GET.get('q')
    if search_data:
        data_dict["username__contains"] = search_data
    else:
        search_data = ""

    # 去数据库搜索
    queryset = models.Admin.objects.filter(**data_dict)

    # 分页
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
        "search_data": search_data
    }
    return render(request, "admin_list.html", context)


def admin_add(request):
    # 添加管理员
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'change.html', {"form": form, "title": title})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # {'username': '刘琪', 'password': '123123', 'confirm_password': '123123'}
        form.save()
        return redirect("/admin/list/")
    return render(request, 'change.html', {"form": form, "title": title})
