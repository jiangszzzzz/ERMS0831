from django.shortcuts import render, redirect

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import AdminModelForm, AdminEditModelForm,AdminResetModelForm


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


def admin_edit(request, nid):
    # 编辑管理员

    # 判断 url 中的 nid 是否在数据库中（可能多人操作时 被删除） 增加判断
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': "数据不存在"})

    title = "编辑管理员"
    if request.method == "GET":
        # form = AdminModelForm(instance=row_object) # 可以复用admin add的form
        form = AdminEditModelForm(instance=row_object)  # instance row object 实现输入时，呈现默认数据
        return render(request, 'change.html', {"form": form, "title": title})
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    # 在Django中使用modelform保存数据时，通常需要传递一个instance参数，以指定要保存的数据库记录。
    # instance参数用于表示要更新或修改的现有记录，如果要创建新记录，则可以不传递instance参数。
    # 如果您传递了instance参数，modelform将根据该instance对象的主键来更新相应的数据库记录。
    # 如果不传递instance参数，modelform将创建一个新的数据库记录。
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, 'change.html', {"form": form, "title": title})


def admin_delete(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': "数据不存在"})
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


def admin_reset(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': "数据不存在"})
    title = "重置密码 - {}".format(row_object.username)

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, 'change.html', {"form": form, "title": title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, 'change.html', {"form": form, "title": title})
