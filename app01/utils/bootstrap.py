from django import forms


class BootstrapModleForm(forms.ModelForm):
    # 给前端加上样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环modelform 的所有字段 给每个字段的插件设置
        for name, field in self.fields.items():
            # 字段中有属性 保留 字段中没有属性 才添加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }


class BootstrapForm(forms.Form):
    # 给前端加上样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环modelform 的所有字段 给每个字段的插件设置
        for name, field in self.fields.items():
            # 字段中有属性 保留 字段中没有属性 才添加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }
