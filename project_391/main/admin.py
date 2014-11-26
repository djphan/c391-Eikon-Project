from django.contrib import admin
from main.models import Persons, Users, Groups, GroupLists, Images, Views

class PersonsAdmin(admin.ModelAdmin):
    pass

class UsersAdmin(admin.ModelAdmin):
    pass

class GroupsAdmin(admin.ModelAdmin):
    pass

class GroupListsAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'group_name':
            kwargs['queryset'] = Groups.objects.exclude(group_name='public')

    list_display = ("group_name", "friend_id")
    
class ImagesAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Users)
admin.site.register(Groups)
admin.site.register(GroupLists)
admin.site.register(Views)
