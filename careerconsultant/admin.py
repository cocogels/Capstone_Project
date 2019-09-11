from django.contrib import admin


from .models import IHE_ContactModel, ICL_ContactModel, SHS_ContactModel, IHE_ContactCategoryModel, ICL_ContactCategoryModel, SHS_ContactCategoryModel

# Register your models here.

admin.site.register(IHE_ContactModel)
admin.site.register(ICL_ContactModel)
admin.site.register(SHS_ContactModel)


admin.site.register(IHE_ContactCategoryModel)
admin.site.register(SHS_ContactCategoryModel)
admin.site.register(ICL_ContactCategoryModel)
