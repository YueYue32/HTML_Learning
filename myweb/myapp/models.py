from django.db import models

# Create your models here.
# from django.db import models
from django.utils import timezone


# 自定義查詢 id
# get_queryset 是繼承models.Manager內的指令，不能亂改
# super()呼叫父類別search_cSex
# 後面再銜接get_queryset.filter(條件)
class search_cSex(models.Manager):
    def get_queryset(self):
        return super(search_cSex,self).get_queryset().filter(cSex__contains = "M")


# 自定義查詢 cAddr
# get_queryset 是繼承models.Manager內的指令，不能亂改
# super()呼叫父類別search_cAddr
# 後面再銜接get_queryset.filter(條件)
class search_cAddr(models.Manager):
    def get_queryset(self):
        return super(search_cAddr,self).get_queryset().filter(cAddr__contains = '台北')



# Create your models here.
class student(models.Model):
    SEX_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]
    cName = models.CharField('姓名',max_length=20, null=False)
    cSex = models.CharField('性別',max_length=1, choices=SEX_CHOICES, default='', null=False)
    cBirthday = models.DateField('生日',null=False)
    cEmail = models.EmailField('Email',max_length=100, blank=True, default='')
    cPhone = models.CharField('手機',max_length=50, blank=True, default='')
    cAddr = models.CharField('地址',max_length=255, blank=True, default='')
    last_modified = models.DateTimeField('最後修改日期', auto_now = True)
    created = models.DateTimeField('保存日期',default = timezone.now)
    objects = models.Manager()
    obj_cSex = search_cSex()
    obj_cAddr = search_cAddr()


    def __str__(self):
        return self.cName