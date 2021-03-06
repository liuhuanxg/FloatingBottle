from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.shortcuts import HttpResponseRedirect
from home.forms import UserForm
from FloatingBottle.common import setPassword, loginValid, send_email, set_page
from string import ascii_letters, digits
import random
from django.db.models import Q, F


@loginValid
def index(request):
    bus_number = Bus.objects.count()
    type_number = BusType.objects.count()
    site_number = Site.objects.count()
    user_id = request.session.get("user_id")
    site_history_list = SiteHistory.objects.filter(user_id=user_id).order_by("count")[0:6]
    bus_history_list = BusHistory.objects.filter(user_id=user_id).order_by("count")[0:6]
    return render(request, "common/index.html",{"bus_number":bus_number,"site_number":site_number,"type_number":type_number,"site_history_list":site_history_list,"bus_history_list":bus_history_list})

# 注册页面
def register(request):
    errors = ""
    if request.method == "POST":
        userform = UserForm(request.POST)                     # 将请求的数据加入表单进行校验
        if userform.is_valid():
            username = userform.cleaned_data.get("username")  # 校验过的数据
            password = userform.cleaned_data.get("password")
            password_confirm = request.POST.get("password_confirm")
            if password == password_confirm:
                # 数据库保存用户注册信息
                user = User()
                user.username = username
                user.password = setPassword(setPassword(password))
                user.save()
            return HttpResponseRedirect("/login/")  # 如果注册成功，跳转到登陆
        else:
            errors = userform.errors
    return render(request, "common/register.html",{"errors":errors})


# 登录
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        u = User.objects.filter(username=username,password=setPassword(setPassword(password)))
        if u.exists():
            response = HttpResponseRedirect("/")
            response.set_cookie("username", username)
            request.session["username"] = username
            request.session["user_id"] = u[0].id
            request.session["image"] = u[0].image.path
            return response
    return render(request, "common/login.html")


# 退出
def logout(request):
    response = HttpResponseRedirect("/login/")
    try:
        response.delete_cookie("username")
        del request.session["username"]
        del request.session["user_id"]
        del request.session["image"]
    except Exception as e:
        pass
    return response

# 个人信息
@loginValid
def user_info(request):
    user_id = request.session.get("user_id")
    user = User.objects.filter(id=user_id)
    if user.exists():
        user = user[0]
        return render(request, "common/user_info.html", locals())
    else:
        return render(request,"common/pages-404.html")



# 修改个人信息
@loginValid
def change_userinfo(request):
    user_id = request.session.get("user_id")
    user = User.objects.filter(id=user_id)

    if not user.exists():
        return render(request, "common/pages-404.html")

    if request.method == "POST":
        data = request.POST
        nick_name = data.get("nick_name")
        gender = data.get("gender")
        phone = data.get("phone")
        email = data.get("email")
        address = data.get("address")
        image = request.FILES.get("image")
        print(image)
        user.update(
            nick_name=nick_name if nick_name else F("nick_name"),
            gender = gender if gender else F("gender"),
            phone = phone if phone else F("phone"),
            email = email if email else F("email"),
            address = address if address else F("address")
        )
        if image:
            user = user[0]
            user.image = image
            user.save()
        return redirect("home:user_info")

    return render(request, "common/change_userinfo.html", {"user":user[0]})


# 修改密码
@loginValid
def change_password(request):
    user_id = request.session.get("user_id")
    error = ""
    if request.method == "POST":
        data = request.POST
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        password_sure = data.get("password_sure")
        user = User.objects.filter(id=user_id,password=setPassword(setPassword(old_password)))
        if new_password == password_sure and user.exists():
            user.update(password=setPassword(setPassword(new_password)))
            return redirect("home:logout")
        else:
            error = "原密码错误或两次密码不一致！"
    return render(request, "common/change_password.html",{"error":error})


# 忘记密码
def forget_password(request):
    error = ""
    if request.method == "POST":
        data = request.POST
        email = data.get("email")
        code = data.get("code")
        password = data.get("password")
        alternative_code = request.session.get("code")
        alternative_email1 = request.session.get("email")
        if email==alternative_email1 and code == alternative_code:
            User.objects.filter(email=email).update(password=setPassword(setPassword(password)))
            return redirect("home:login")
        error = "邮箱或验证码不正确，请确认！"
    return render(request, "common/forget_password.html",{"error":error})


# ajax 发送验证码
def send_code(request):
    response = {"status":0, "data":"邮箱有误，请确认邮箱"}
    email = request.GET.get("email")
    u = User.objects.filter(email=email)
    if u.exists():
        alternate_string = ascii_letters + digits
        str1 = ""
        for i in range(6):
            str1 += random.choice(alternate_string)
        print(str1)
        result = send_email(str1,email)
        if result:
            response["status"] = 1
            response["data"] = "验证码已发送，请查收"
            request.session["code"] = str1
            request.session["email"] = email
    return JsonResponse(response)



# 公交信息
@loginValid
def bus_message(request):
    type_name = request.GET.get("type_name","")
    bus_name = request.GET.get("bus_name","")
    if bus_name or type_name:
        bus_list = Bus.objects.filter(Q(bus_name__icontains=bus_name) or Q(type__type_name__icontains=type_name)).order_by("id")
    else:
        bus_list = Bus.objects.all().order_by("id")
    page = request.GET.get("page", 0)
    data, page_list = set_page(bus_list, 20, page)
    return render(request, "common/bus_message.html", {"data": data, "page_list": page_list,"type_name":type_name, "bus_name":bus_name})


# 公交详情
@loginValid
def bus_detail(request,id):
    bus = Bus.objects.filter(id=id)
    if not bus.exists():
        return render(request, "common/pages-404.html")
    bus = bus[0]
    site_list = BusSite.objects.filter(bus=id).order_by("level").values_list("site_id",flat=True)
    s_list = Site.objects.filter(id__in=site_list)
    site_result = []
    for s in s_list:
        dict1 = {"site_name":s.site_name,"bus_list":[]}
        bus_list = BusSite.objects.filter(site=s.id).exclude(bus=bus.id)
        for b in bus_list:
            dict1["bus_list"].append({"bus_name":b.bus.bus_name,"id":b.bus.id})
        site_result.append(dict1)
    user_id = request.session.get("user_id")
    b = BusHistory.objects.filter(user=user_id, bus=bus.id)
    if b.exists():
        b.update(count=F("count") + 1)
    else:
        BusHistory.objects.create(user_id=user_id, bus_id=bus.id, count=1)
    return render(request, "common/bus_detail.html", {"s_list": site_result,"bus":bus})


# 站台信息
@loginValid
def site_message(request):
    site_name = request.GET.get("site_name","")
    if site_name:
        site_list = Site.objects.filter(site_name__icontains=site_name).order_by("id")
    else:
        site_list = Site.objects.all().order_by("id")
    page = request.GET.get("page", 0)
    data, page_list = set_page(site_list, 20, page)
    return render(request, "common/site_message.html", {"data": data, "page_list": page_list,"site_name":site_name})

# 站点详情
@loginValid
def site_detail(request,id):
    site = Site.objects.filter(id=id)
    if not site.exists():
        return render(request, "common/pages-404.html")
    site = site[0]
    user_id = request.session.get("user_id")
    s = SiteHistory.objects.filter(user=user_id,site=site.id)
    if s.exists():
        s.update(count=F("count")+1)
    else:
        SiteHistory.objects.create(user_id=user_id, site_id=site.id, count=1)
    return render(request, "common/site_detail.html", {"site":site})

# ajax 删除浏览记录
def del_history(request):
    type = request.GET.get("type")
    id = request.GET.get("id")
    print(type, id)
    if type =="Bus":
        result = BusHistory.objects.filter(id=id).delete()
    else:
        result = SiteHistory.objects.filter(id=id).delete()
    if result:
        response = {"status": 1}
    else:
        response = {"status": 0}
    return JsonResponse(response)