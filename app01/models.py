from django.db import models


# Create your models here.

class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return self.title


class User_info(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")

    # 有约束 django 写 depart 生成  depart_id
    # 有约束                    to 与那张表关联    to_field 表中的一列关联        级联删除
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    # 有约束                    to 与那张表关联    to_field 表中的一列关联        置空
    # depart = models.ForeignKey(id="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    # django 代码中约束
    gender_choices = ((1, "男"), (2, "女"),)
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
