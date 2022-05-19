from django.contrib import admin

from user.models import Answer, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['tg_id','full_name','link','tag']
# Register your models here.
admin.site.register([Answer])