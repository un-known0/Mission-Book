from django.db import models

# Create your models here.
class Checklist(models.Model):
    title = models.CharField(max_length=50) #체크리스트 제목
    category = models.IntegerField(default=0) #체크리스트 분류 1=학업 2=친목 3=경험
    is_complete_num = models.BooleanField(default=False) #complete_num의 유효여부
    complete_num = models.IntegerField(default=0) #완료에 필요한 개수
    class_reward = models.FloatField(default=0) #성공시 증가하는 학업스탯
    social_reward = models.FloatField(default=0) #성공시 증가하는 사교스탯
    exp_reward = models.FloatField(default=0) #성공시 증가하는 경험스탯
    total_exp_reward = models.FloatField(default=0) #성공시 증가하는 경험치
    level = models.IntegerField(default=1) #난이도
    content = models.CharField(max_length=100) #체크리스트 내용
    need_class_stat = models.FloatField(default=0) #미션 개방 학업스탯
    need_social_stat = models.FloatField(default=0) #미션 개방 사교스탯
    need_exp_stat = models.FloatField(default=0) #미션 개방 경험스탯
    
    def __str__(self):
        return f'<{self.category}>{self.title}'
    
class MemberChecklist(models.Model):
    member = models.CharField(max_length=20)
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    status = models.IntegerField(default=-1)    