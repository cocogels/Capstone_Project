from django.contrib import admin

from .models import TargetSheet, PaymentDetails, SanctionSetting, CommissionSetting, SchoolYear
from .forms import TargetSheetForm, SchoolYearForm, PaymentDetailsForm, SanctionSettingForm
# Register your models here.
from .widgets import CustomDatePickerInput
from django.db import models as db_models
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
    


class SchoolYearAdmin(admin.ModelAdmin):
    formfield_overrides = {
         db_models.DateField: {'widget': CustomDatePickerInput},
     }
    form = SchoolYearForm
    list_display = (
    'start_year',
    'end_year',

    )
    
    
  
class PaymentDetailsAdmin(admin.ModelAdmin):
    form = PaymentDetailsForm
    fieldsets =(
        (
            "Matriculation",
            {   
                'fields':
                    (
                        'status',
                        'course',
                        'cash_amount_per_unit',
                        'cash_miscellaneous_fee',
                        'cash_lab_fee',
                        'cash_registration_fee',
                        'ins_amount_unit',
                        'ins_miscellaneous_fee',
                        'ins_lab_fee',
                        'ins_registration_fee',

                    ),
            },
        ),
    )
    list_display = (
        'status',
        'course',
    )

class SactionAdmin(admin.ModelAdmin):
    form = SanctionSettingForm
    list_display = (
        'date_created',
        'first_sanction',
    )
    
    
admin.site.register(SchoolYear, SchoolYearAdmin)
admin.site.register(PaymentDetails, PaymentDetailsAdmin)
admin.site.register(SanctionSetting, SactionAdmin)
admin.site.register(CommissionSetting)
admin.site.register(TargetSheet, TargetSheetAdmin)
