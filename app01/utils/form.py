from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from app01.utils.bootstrap import BootstrapModleForm


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
