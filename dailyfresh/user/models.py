from django.db import models
from django.db.models import Q
from rest_framework.exceptions import NotFound


class UserModel(models.Model):
    u_name = models.CharField(max_length=32,unique=True,null=False,blank=False)
    u_password = models.CharField(max_length=64)
    u_email = models.CharField(max_length=64,null=False,blank=False)
    u_icon = models.CharField(max_length=256,null=True,blank=False,default="") #头像
    is_delete = models.BooleanField(default=False)  #是否删除
    is_active = models.BooleanField(default=False) #是否激活


    @classmethod
    def check_username(cls,u_name):
        # 检测用户名在数据库中是否存在,如果存在则返回true,false反之
        return UserModel.objects.filter(u_name=u_name).exists()  #验证用户名是否存在

    @classmethod
    def get_user(cls,u_user):  #根据u_user进行查询
        """

        :param U_user: 用户标示,可能是用户名或者邮箱
        :return:
        """
        user = UserModel.objects.filter(Q(u_name=u_user) | Q(u_email=u_user)).first()
        if not user:
            raise NotFound(detail="用户不存在")
        return user #如果用户存在返回user

    def check_password(self,u_password):  #获取密码
        return self.u_password == u_password



    class Meta:
        db_table = "user_model"