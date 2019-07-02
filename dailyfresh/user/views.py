from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template import loader
from rest_framework.exceptions import APIException, ValidationError, AuthenticationFailed, PermissionDenied
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from common.token_generate import generate_token
from dailyfresh.settings import USER_TOKEN_TIMEOUT, EMAIL_HOST_USER, SERVER_HOST, ACTIVATE_TIMEOUT
from user.models import UserModel
from user.serializer import UserSerializer


class UsersView(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class =  UserSerializer

    def get(self,request,*args,**kwargs):   #激活接口
        action = request.query_params.get("action")
        if action == "activate":
            try:
                token = request.query_params.get("token")  #获取token
                u_name = cache.get(token)  #获取u_name
                if u_name:  #判断u_name是否有数据
                    cache.delete(token)   #有就删除
                user = UserModel.get_user(u_name)
                user.is_active = True
                user.save()
            except Exception as e :
                print(e)

            # return redirect("/index/")
            return  render(request,"index.html")


    def post(self,request,*args,**kwargs):  #重写post
        action = request.query_params.get("action")

        if action == "register":
            return self.do_register(request,*args,**kwargs)
        elif action =="login":
            return self.do_login(request,*args,**kwargs)
        elif action == "check_username":
            return self.check_user_name(request,*args,**kwargs)
        elif action == "check_email":
            # return self.check_user_email(request,*args,**kwargs)
            pass
        elif action == "modify_info":
            pass
        elif action == "modify_icon":
            pass
        elif action == "get_info":
            pass
        else:
            raise APIException(detail="请提供正确的动作")

    def do_register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        u_email = serializer.data.get("u_email")
        u_name = serializer.data.get("u_name")


        subject = "天天生鲜用户激活邮件"  #邮件主题
        msg = "恭喜你,激活成功!请登录"  #激活链接 中的内容

        activate_email = loader.get_template("activate.html") #渲染邮件内容模板

        token = generate_token()  #生成token
        cache.set(token,u_name,timeout=ACTIVATE_TIMEOUT) #存储token在缓存

        activate_url = SERVER_HOST + "/users/?action=activate&token="+token
        html_msg = activate_email.render({"u_name":u_name,"activate_url":activate_url})

        send_mail(subject=subject,message=msg,from_email=EMAIL_HOST_USER,recipient_list=(u_email,),html_message=html_msg)

        data = {
            "msg": "创建成功",
            "status": HTTP_201_CREATED,
            "data": serializer.data
        }
        return Response(data, HTTP_201_CREATED, headers=headers)

    def do_login(self, request, *args, **kwargs):
    #登录-->就是验证用户名 密码邮箱等是否存在,并验证输入的是否正确, 验证账户的激活状态激活后才能登录
        u_user = request.data.get("u_user")  #用户名标示
        u_password = request.data.get("u_password")

        user = UserModel.get_user(u_user)

        if not user.check_password(u_password):
            raise AuthenticationFailed(detail="密码错误")   #AuthenticationFailed 认证失败

        if not user.is_active:   #判断用户是否 激活
            raise PermissionDenied(detail="用户未激活") #权限拒绝


        token =generate_token()
        cache.set(token,user,timeout=USER_TOKEN_TIMEOUT)  #用户过期时间
        data ={
            "msg":"登录成功",
            "status":HTTP_200_OK,
            "data":{
                "token":token
            }
        }
        return Response(data)

    def check_user_name(self,request,*args,**kwargs):
        u_name = request.data.get("u_name") #获取u_name

        if UserModel.check_username(u_name): #如果存在u_name存在就抛异常
            raise ValidationError(detail="用户名已存在")

        data = {
            "status":HTTP_200_OK,
            "msg":"用户名可用"
        }
        return Response(data)  #如果不存在,表示用户名可用

