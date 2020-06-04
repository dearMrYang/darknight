import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
from apps.baseModel import BaseModel


class UserManager(BaseUserManager):
    def _create_user(self, username, password, **kwargs):
        if not username:
            raise ValueError('请传入用户名！')
        if not password:
            raise ValueError('请传入密码！')
        uid = uuid.uuid3(uuid.NAMESPACE_DNS, username).hex
        user = self.model(username=username, **kwargs)
        user.uid = uid
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username, password, **kwargs)

    def create_superuser(self, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username, password, **kwargs)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(verbose_name='ID')
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.URLField(default='/static/images/avatar.png')

    objects = UserManager()
    # 验证时，username
    USERNAME_FIELD = 'username'
    # 创建user时，需要填写的字段 USERNAME_FIELD+REQUIRED_FIELDS+password
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'db_user'
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
