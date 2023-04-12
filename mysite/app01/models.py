from django.db import models


# Create your models here.

class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='标题', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    account = models.DecimalField(verbose_name='账户余额', max_digits=10, decimal_places=2)
    create_time = models.DateField(verbose_name="创建时间")
    # 外键约束
    # 数据库中会自动给depart加id=depart_idn
    # depart=models.ForeignKey(to="Department",to_field="id")
    # 1.联级删除
    # depart=models.ForeignKey(to="Department",to_field="id",on_delete=models.CASCADE())
    # 2.置空
    depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.SET_NULL, null=True, blank=True)
    # django中做约束
    gender_choices = {
        (1, "男"),
        (2, "女"),
    }
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号", max_length=11)  # 存为字符串，方便后面正则表达式检验
    price = models.IntegerField(verbose_name="价格")
    level_choices = {
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    }
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    status_choices = (
        (1, "已占用"),
        (2, "未使用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Admin(models.Model):
    """管理员"""
    username=models.CharField(verbose_name="用户名",max_length=32)
    password=models.CharField(verbose_name="密码",max_length=64)
