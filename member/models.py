from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class MemberManager(BaseUserManager):
    def create_user(self, id, password=None, **extra_fields):
        if not id:
            raise ValueError('이미 존재하는 ID입니다.')
        user = self.model(id=id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, password=None, **extra_fields):
        raise NotImplementedError('This model does not support superuser creation.')


class Member(AbstractBaseUser):
    id = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=20)
    int_stat = models.IntegerField(default=0)
    social_stat = models.IntegerField(default=0)
    exp_stat = models.IntegerField(default=0)
    total_exp = models.IntegerField(default=0)
    title = models.ForeignKey('Title', on_delete=models.SET_NULL, null=True)
    title_color = models.IntegerField(default='0')
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = MemberManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return False

    def has_module_perms(self, app_label):
        return False
    

class Title(models.Model):
    name = models.TextField()
    need_int = models.IntegerField()
    need_social = models.IntegerField()
    need_exp = models.IntegerField()
    need_total_exp = models.IntegerField()


