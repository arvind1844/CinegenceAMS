from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

admin.site.site_header  =  "Cinegence Admin"  
admin.site.site_title  =  "Asset Management"
admin.site.index_title  =  "Asset Management System"

class IndividualAssestAdmin(admin.StackedInline):
    model = IndividualAssest

@admin.register(Assests)
class AssestsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    search_fields = ['title']
    inlines = [IndividualAssestAdmin]

    class Meta:
        model = Assests


class IndividualAssestAdmin(admin.ModelAdmin):
    pass

class ContactAdmin(ImportExportModelAdmin):
    pass

    class Meta:
        model = Contact

class WorkDetailsAdmin(ImportExportModelAdmin):
    pass

    class Meta:
        model = Work_Details

admin.site.register(Work_Details, WorkDetailsAdmin)
admin.site.register(ExtendedUser)
admin.site.register(Contact, ContactAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)
