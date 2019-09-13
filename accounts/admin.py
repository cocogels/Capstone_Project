from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserMarketingProfile, Profile
from .forms import EmployeeCreationForm, MarketingAdminUserChangeForm
# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = MarketingAdminUserChangeForm
    add_form = EmployeeCreationForm
    fieldsets = (
        (
            None,
            {
                "fields": ('email',),
            },
        ),
        (
            "Permissions",
            {
                "fields":
                    (
                        "is_active",
                        "is_staff",
                        "is_superuser",
                        "is_centermanager",
                        "is_centerbusinessmanager",
                        "is_marketinghead",
                        "is_registrar",
                        'is_budgetary',
                        'is_ihe',
                        'is_shs',
                        'is_icl',
                        "user_permissions",
                    )
            },
        ),
        (
            "Important dates",
            {
                "fields":
                    (
                        "last_login",
                        "date_joined",
                    )
            },
        ),
    )

    exclude = ['username']
    readonly_fields = ('last_login', "date_joined",)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields":
                    (
                        "email",
                        "password",

                ),
            },
        ),
    )

    list_display = (
        "email",
        "is_staff",
        "is_active"
    )

    search_fields = (
        "email",
    )

    ordering = (
        "email",
    )

    filter_horizontal = ()



admin.site.register(UserMarketingProfile, UserAdmin)
admin.site.register(Profile)
admin.site.unregister(Group)


"""-----------------------------------------------------"""






admin.site.site_header = 'Marketing Administration'
admin.site.site_title = 'Marketing Administration'
