from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from checklist.models import Checklist,MemberChecklist


class MemberManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):

        if not user_id:
            raise ValueError('이미 존재하는 ID입니다.')
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(user_id, password, **extra_fields)


class Member(AbstractBaseUser):
    user_id = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=20)
    int_stat = models.FloatField(default=0)
    social_stat = models.FloatField(default=0)
    exp_stat = models.FloatField(default=0)
    total_exp = models.FloatField(default=1)
    title = models.ForeignKey('Title', on_delete=models.SET_NULL, null=True, blank=True)
    title_color = models.IntegerField(default=0)
    profile_image = models.ImageField(upload_to="images/", null=True, blank=True, default="images/lion1.jpg")
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)


    objects = MemberManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def can_select_title(self, title):
        if self.title == title:
            return False
        elif (self.int_stat >= title.need_int and
              self.social_stat >= title.need_social and
              self.exp_stat >= title.need_exp and
              self.total_exp >= title.need_total_exp):
            return True
        else:
            return False    
    
    def can_graduation(self, graduation):
        if (self.int_stat >= graduation.need_int and
              self.social_stat >= graduation.need_social and
              self.exp_stat >= graduation.need_exp and
              self.total_exp >= graduation.need_total_exp):
            return True
        else:
            return False
        
        
class Title(models.Model):
    name = models.TextField()
    need_int = models.IntegerField(default=0)
    need_social = models.IntegerField(default=0)
    need_exp = models.IntegerField(default=0)
    need_total_exp = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name    


class Graduation(models.Model):
    name = models.TextField()
    content = models.TextField()
    need_int = models.IntegerField(default=0)
    need_social = models.IntegerField(default=0)
    need_exp = models.IntegerField(default=0)
    need_total_exp = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name     