from django.contrib import admin

# Register your models here.
from myapp.models import student

from django.utils.translation import gettext_lazy as _



# admin.site.register(student) # 最簡易的顯示

class Morethan4(admin.SimpleListFilter):
    title = _('id')
    parameter_name = 'compareid'  # url最先要接的參數

    def lookups(self, request, model_admin):
        return (
            ('>4', _('id > 4')),  # 前方對應下方'>50'(也就是url的request)，第二個對應到admin顯示的文字
            ('<4', _('id < 4')),
        )

    # 定義查詢時的過濾條件
    def queryset(self, request, queryset):
        if self.value() == '>4':
            return queryset.filter(id__gt=3)
        if self.value() == '<4':
            return queryset.filter(id__lt=4)


class studentAdmin(admin.ModelAdmin):
    list_display=('id','cName','cSex','cBirthday','cEmail','cPhone','cAddr')
    # list_filter=('cSex',)
    search_fields=('cName','cEmail','cPhone',)
    ordering=('id','cName',)
    list_filter = (Morethan4,)



admin.site.register(student, studentAdmin)


