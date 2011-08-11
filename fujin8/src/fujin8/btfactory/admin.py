from models import MonthlyLink,MovieLink,Actress,DailyLink 
from django.contrib import admin

class MonthlyLinkAdmin(admin.ModelAdmin):
    #inlines = [ChoiceInline]
    list_display = ('link', 'enable')
    list_filter = ['enable']

admin.site.register(MonthlyLink,MonthlyLinkAdmin)
admin.site.register(MovieLink)
admin.site.register(Actress)
admin.site.register(DailyLink)