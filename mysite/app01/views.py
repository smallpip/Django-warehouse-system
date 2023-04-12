import hashlib
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from app01 import models
from django import forms

# 部门
from django.utils.safestring import mark_safe

from app01.utils.pagination import Pagination

from app01.utils.bootModelform import BootModelForm

from app01.utils.encrypt import md5

from app01.utils.bootModelform import BootForm

from app01.utils.code import check_code


def depart_list(request):
    """部门列表"""
    queryset = models.Department.objects.all()
    # for obj in queryset:
    #     obj.depart_id
    #     obj.depart.title#自动获取对象的在其他表的部门名称

    # 2.实例化分页对象
    page_object = Pagination(request, queryset, page_size=8)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'depart_list.html', context)


def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request, 'depart_add.html')
    # 获取用户post提交来的数据
    title = request.POST.get("title")
    # 保存到数据库
    models.Department.objects.create(title=title)
    # 重定向部门列表
    return redirect("/depart/list/")


def depart_delete(request):
    """删除部门"""
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """修改部门"""
    # 根据nid，获取他的数据
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {"row_object": row_object})
    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")


# 用户
def user_list(request):
    """用户管理"""
    queryset = models.UserInfo.objects.all()
    # for obj in queryset:
    #     obj.depart_id
    #     obj.depart.title#自动获取对象的在其他表的部门名称

    # 2.实例化分页对象
    page_object = Pagination(request, queryset, page_size=10)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'user_list.html', context)


def user_add(request):
    """添加用户"""
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, "user_add.html", context)
    # 获取用户提交的数据
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    acount = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gender_id = request.POST.get('dp')
    depart_id = request.POST.get('dp')

    # 添加到数据库中
    models.UserInfo.objects.create(name=user, password=pwd, age=age,
                                   account=acount, create_time=ctime,
                                   gender=gender_id, depart_id=depart_id)
    return redirect("/user/list/")


#################### modelform #############################


class UserModelForm(forms.ModelForm):
    # 只能在这添加额外的约束
    # name=forms.CharField(min_length=3,label="用户名")
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]
        # widgets={
        #     "name":forms.TextInput(attrs={"class":"form-control"}),
        #     "password":forms.PasswordInput(attrs={"class":"form-control"}),
        #     "age":forms.TextInput(attrs={"class":"form-control"})
        # }

    # 等于上面代码
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
def user_modeform_add(request):
    """添加用户（modelform）"""
    if request.method == "GET":
        form = UserModelForm
        return render(request, "user_model_form_add.html", {"form": form})
    # 用户post提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # 如果数据合法，提交到数据库
        form.save()  # 不用create
        return redirect("/user/list/")
    else:
        print(form.errors)
        return render(request, "user_model_form_add.html", {"form": form})


def user_edit(request, nid):
    # 获取nid要编辑那一行的数据
    rbj = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=rbj)
        return render(request, "user_model_form_edit.html", {"form": form})
    form = UserModelForm(data=request.POST, instance=rbj)
    if form.is_valid:
        # 想要用户输入以外再增加值
        # form.instance.字段名=值
        form.save()
        return redirect("/user/list/")


def user_del(request):
    nid = request.GET.get('nid')
    product = models.UserInfo.objects.filter(id=nid).first()
    product.delete()

    return redirect("/user/list/")


def pretty_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'pretty_list.html', context)


class PrettyModelForm(BootModelForm):
    # 验证方式1
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'1[3-9]\d{9}$', '手机号格式错误')]

    )
    # 验证方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        # 排除自身
        # exists=models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile
def pretty_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list')
    else:
        return render(request, "pretty_add.html", {"form": form})

class Pretty_edit_ModelForm(BootModelForm):
    # 验证方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']
        # fields="__all__"
        # exclude=['level']#排除
def pretty_edit(request, nid):
    """"靓号编辑"""
    rbj = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = Pretty_edit_ModelForm(instance=rbj)
        return render(request, "pretty_edit.html", {"form": form})
    form = Pretty_edit_ModelForm(data=request.POST, instance=rbj)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list')
    else:
        return render(request, "pretty_edit.html", {"form": form})


def pretty_del(request):
    nid = request.GET.get('nid')
    rbj = models.PrettyNum.objects.filter(id=nid).all()
    rbj.delete()
    return redirect('/pretty/list')

#管理员
def admin_list(request):
    """管理员列表"""
    #检查用户是否已经登录，如果未登录，跳转回登陆界面
    #用户发来请求,获取cookie随机字符串，拿字符串来看看session中有没有，如果有，则表示登陆过
    info=request.session.get("info")
    print(info)
    if not info:
        return redirect('/login')
    queryset=models.Admin.objects.all()
    page_object=Pagination(request,queryset)
    context={
        'queryset':page_object.page_queryset,
        'page_string':page_object.html()
    }
    return render(request,"admin_list.html",context)

class AdminModelForm(BootModelForm):
    confirm_password=forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)#保留输错的值,
    )
    class Meta:
        model=models.Admin
        fields=["username","password","confirm_password"]
        widgets={
            "password":forms.PasswordInput(render_value=True)#隐藏值
        }
    def clean_password(self):
        pwd=self.cleaned_data.get("password")
        md5_pwd=md5(pwd)
        #检验当前密码和数据库是否一致，一致则不用修改
        exists=models.Admin.objects.filter(id=self.instance.pk,password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能和以前一致")
        return md5_pwd
    def clean_confirm_password(self):
        confirm=md5(self.cleaned_data.get("confirm_password"))
        pwd=self.cleaned_data.get("password")
        if confirm!=pwd:
            raise ValidationError("密码不一致")
        return confirm
def admin_add(request):
    """添加管理员"""
    title="新建管理员"
    if request.method=="GET":
        form=AdminModelForm()
        return  render(request,"change.html",{"title":title,"form":form})

    form=AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    else:
        return render(request,'change.html',{'form':form,'title':title})

class Admin_EDIT_ModelForm(BootModelForm):
    class Meta:
        model=models.Admin
        fields=["username"]

def admin_edit(request,nid):
    """编辑管理员"""
    #如果获取不到，则得到none
    rbj=models.Admin.objects.filter(id=nid).first()
    if not rbj:
        return render(request,'error.html',{"msg":"数据不存在"})
    title="编辑管理员"
    if request.method=="GET":
        form = Admin_EDIT_ModelForm(instance=rbj)
        return render(request,'change.html',{"title":title,"form":form})
    form=Admin_EDIT_ModelForm(data=request.POST,instance=rbj)
    if form.is_valid():
        form.save()
        return  redirect("/admin/list")
    return render(request, 'change.html', {"title": title, "form": form})

def admin_del(request):
    """删除管理员"""
    nid=request.GET.get('nid')
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list')

class Admin_res_ModelForm(AdminModelForm):
    class Meta:
        model=models.Admin
        fields=["password","confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)  # 隐藏值
        }
def admin_reset(request,nid):
    """重置密码"""
    rbj=models.Admin.objects.filter(id=nid).first()
    if not rbj:
        redirect("/admin/list")
    title="重置密码-{}".format(rbj.username)
    if request.method=="GET":
        form=Admin_res_ModelForm()
        return render(request,'change.html',{"title":title,"form":form})
    form=Admin_res_ModelForm(data=request.POST,instance=rbj)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    return render(request, 'change.html', {"title": title, "form": form})

#登录
class LoginForm(BootForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

def login(request):
    """登录界面"""
    if request.method=="GET":
        form=LoginForm()
        return render(request,'login.html',{"form":form})

    form=LoginForm(data=request.POST)
    if form.is_valid():

        #验证码验证
        user_input_code=form.cleaned_data.pop('code')
        print(form.cleaned_data)
        img_code=request.session.get('image_code','')
        if img_code!=user_input_code:
            form.add_error("code","验证码错误")
            return render(request, 'login.html', {"form": form})
        # 密码验证
        adj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not adj:
            form.add_error("password","用户名密码错误")
            return render(request, 'login.html', {"form": form})
        #用户名和密码正确
        #网站生成随机字符串，写到用户浏览器的cookie中,再写道session中
        request.session["info"]={'id':adj.id,'name':adj.username}
        return redirect('/user/list')

    return render(request,'login.html',{"form":form})



def logout(request):
    """注销"""
    request.session.clear()

    return redirect('/login')

from PIL import Image,ImageDraw,ImageFont

def image_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


