from django.contrib import admin
from main.models import Users, Groups, GroupLists, Images

# Register your models here.
admin.site.register(Users)
admin.site.register(Groups)
admin.site.register(GroupLists)
admin.site.register(Images)
