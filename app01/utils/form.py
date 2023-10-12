from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from app01.utils.bootstrap import BootstrapModleForm
from app01.utils.encrypt import md5


class UserModleForm(BootstrapModleForm):
    name = forms.CharField(min_length=2, label="用户名")

    # 生成前端输入框
    class Meta:
        model = models.User_info
        fields = ["name", "gender", "password", "age", "account", "create_time", "depart", ]


class PrettyNumModleForm(BootstrapModleForm):
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


class PrettyNumEidtModleForm(BootstrapModleForm):
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


class AdminModelForm(BootstrapModleForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        # 增加密码输入插件
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return md5(password)

    def clean_confirm_password(self):
        # print(self.cleaned_data)
        # {'username': '李万', 'password': '123123', 'confirm_password': '123123'}
        password = self.cleaned_data.get("password")
        confirm_password = md5(self.cleaned_data.get("confirm_password"))
        if password != confirm_password:
            raise ValidationError("密码不一致")
        return confirm_password


class AdminEditModelForm(BootstrapModleForm):
    class Meta:
        model = models.Admin
        # 不允许编辑密码 只允许编辑用户名
        fields = ["username"]


class AdminResetModelForm(BootstrapModleForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        # 不允许编辑密码 只允许编辑用户名
        fields = ["password"]
        # 增加密码输入插件
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        md5_password = md5(password)

        # 实现修改密码时 不能与之前密码一致的校验

        # self.instance 表示当前这个对象。 pk 表示 id
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_password).exists()

        if exists:
            raise ValidationError("不能与之前密码一致")
        return md5_password

    def clean_confirm_password(self):
        # print(self.cleaned_data)
        # {'username': '李万', 'password': '123123', 'confirm_password': '123123'}
        password = self.cleaned_data.get("password")
        confirm_password = md5(self.cleaned_data.get("confirm_password"))
        if password != confirm_password:
            raise ValidationError("密码不一致")
        return confirm_password
