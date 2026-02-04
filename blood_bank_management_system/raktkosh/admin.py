from django.contrib import admin

from raktkosh.models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Stock)
admin.site.register(BloodRequest)
admin.site.register(BloodDonate)
admin.site.register(Contact)