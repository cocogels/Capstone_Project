from django.contrib import admin

from .models import TargetSheet, SchoolYearManager, SanctionSetting
from .forms import TargetSheetForm, SanctionSettingForm
# Register your models here.

class TargetSheetAdmin(admin.ModelAdmin):
    form = TargetSheetForm
    fieldsets =(
        (
            "TargetSheet",
            {
                'fields':
                    (
                        'corporate',
                        'retail',
                        'owwa',
                        'seniorhigh',
                        'higher_ed',
                    ), 
            },
        ),
    ) 
    
    list_display = (
        'date_created',
        'corporate',
        'retail',
        'owwa',
        'seniorhigh',
        'higher_ed',
    )
    
    search_fields = (
        'corporate',
        'retail',
        'owwa',
        'seniorhigh',
        'higher_ed',
    )
    

class SactionAdmin(admin.ModelAdmin):
    form = SanctionSettingForm
    list_display = (
        'date_created',
        'first_sanction',
    )
    
    
#admin.site.register(SchoolYear)

admin.site.register(SanctionSetting, SactionAdmin)
admin.site.register(TargetSheet, TargetSheetAdmin)
