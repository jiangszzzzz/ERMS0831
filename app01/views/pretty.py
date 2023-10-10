from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModleForm, PrettyNumModleForm, PrettyNumEidtModleForm


def pretty_list(request):
    # 随机创建500条数据
    # for i in range(10):
    #     for j in range(10):
    #         for k in range(5):
    #             mobile = '18188886' + str(i) + str(j) + str(k)
    #             models.PrettyNum.objects.create(mobile=mobile, price=10, level=1, status=1)

    # 相当于 select * from 表 order by level desc

    # queryset = models.PrettyNum.objects.all().order_by("-level")
    # queryset = models.PrettyNum.objects.all()

    # 搜索框
    data_dict = {}
    search_data = request.GET.get('q')
    if search_data:
        data_dict["mobile__contains"] = search_data
    else:
        search_data = ""
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset, page_size=10)

    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 分完也的数据
        "page_string": page_object.html(),  # 页码
    }
    return render(request, "pretty_list.html", context)


############################## 靓号提交 先建form类

def pretty_add(request):
    title = "新建靓号"
    if request.method == "GET":
        form = PrettyNumModleForm()
        return render(request, "change.html", {"form": form, "title":title})

    form = PrettyNumModleForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, "change.html", {"form": form, "title":title})


# 编辑 form 类


def pretty_edit(request, nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyNumEidtModleForm(instance=row_object)
        return render(request, "pretty_edit.html", {"form": form})

    form = PrettyNumEidtModleForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")
