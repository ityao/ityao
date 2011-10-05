from models import MonthlyLink,MovieLink,Actress,DailyLink 
from django.contrib import admin

class MonthlyLinkAdmin(admin.ModelAdmin):
    #inlines = [ChoiceInline]
    list_display = ('link', 'enable')
    list_filter = ['enable']
    
class ActressAdmin(admin.ModelAdmin):    
    list_display = ('id','admin_thumbnail','name', 'co_names', 'profile')
    search_fields = ['co_names']

class MovieLinkAdmin(admin.ModelAdmin):    
    list_display = ('id','admin_thumbnail','title','actress_names','parsed','create_date','downloadlink')

admin.site.register(MonthlyLink,MonthlyLinkAdmin)
admin.site.register(MovieLink,MovieLinkAdmin)
admin.site.register(Actress,ActressAdmin)
admin.site.register(DailyLink)