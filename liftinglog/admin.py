from liftinglog.models import Log, Lift
from django.contrib import admin
from django.contrib.auth.models import User

class LiftInline(admin.TabularInline):
    model = Lift
    extra = 6

class LogAdmin(admin.ModelAdmin):
    
    list_display = ('pub_date', 'notes')
    

    inlines = [LiftInline]
    list_filter = ['pub_date']
    
    date_hierarchy = 'pub_date'

admin.site.register(Log, LogAdmin) 
admin.site.register(Lift)
