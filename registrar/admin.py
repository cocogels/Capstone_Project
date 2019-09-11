from django.contrib import admin
from .models import RequirementsModel, AvailableCourseModel, AvailableCourseCategory, RequirementsCategory
# Register your models here.



admin.site.register(RequirementsModel)
admin.site.register(AvailableCourseModel)
admin.site.register(AvailableCourseCategory)
admin.site.register(RequirementsCategory)
