from django.shortcuts import render, redirect
from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


def depart_list(request):
    """部门列表"""
    # 去数据库中获得所有部门表
    # [对象，对象]
    queryset = models.Department.objects.all()

    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request, 'depart_add.html')

    title = request.POST.get("title")
    models.Department.objects.create(title=title)

    return redirect("/depart/list/")


def depart_delete(request):
    """删除部门"""
    # http://127.0.0.1:8000/depart/delete/?nid=1
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """修改部门"""
    # http://127.0.0.1:8000/depart/1/edit/
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, "depart_edit.html", {"row_object": row_object})
    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")


def user_list(request):
    queryset = models.User_info.objects.all()
    return render(request, "user_list.html", {"queryset": queryset})


# ##################################  modleForm 实现   ##################################
class UserModleForm(forms.ModelForm):
    name = forms.CharField(min_length=2, label="用户名")

    # 生成前端输入框
    class Meta:
        model = models.User_info
        fields = ["name", "gender", "password", "age", "account", "create_time", "depart", ]

    # 给前端加上样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


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


def pretty_list(request):

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
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    return render(request, "pretty_list.html", {"queryset": queryset, "search_data": search_data}, )


############################## 靓号提交 先建form类
class PrettyNumModleForm(forms.ModelForm):
    # name = forms.CharField(min_length=2, label="用户名")
    #####    验证方式一
    ####     字段 + 正则匹配
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    # )

    # 生成前端输入框
    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status", ]

    # 给前端加上样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    ### 验证方式二 构造方法
    def clean_mobile(self):
        text_mobile = self.cleaned_data["mobile"]

        # 验证是否为相同号码
        exists = models.PrettyNum.objects.filter(mobile=text_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        if len(text_mobile) != 11:
            # 验证不通过
            raise ValidationError("长度错误")
        #  验证通过 把用户输入的值返回
        return text_mobile


def pretty_add(request):
    if request.method == "GET":
        form = PrettyNumModleForm()
        return render(request, "pretty_add.html", {"form": form})

    form = PrettyNumModleForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, "pretty_add.html", {"form": form})


# 编辑 form 类
class PrettyNumEidtModleForm(forms.ModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号")

    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    # 生成前端输入框
    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status", ]

    # 给前端加上样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    #  验证是否为重复号码， 但是要排除自己   编辑和添加时候 条件是不一样的
    def clean_mobile(self):
        text_mobile = self.cleaned_data["mobile"]

        # 验证是否为相同号码    但是要排除自己 .exclude()
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=text_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        if len(text_mobile) != 11:
            # 验证不通过
            raise ValidationError("长度错误")
        #  验证通过 把用户输入的值返回
        return text_mobile


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
