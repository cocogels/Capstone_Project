from django.contrib import admin

from .models import TargetSheet, PaymentDetails, SanctionSetting, CommissionSetting
# Register your models here.

admin.site.register(TargetSheet)
admin.site.register(PaymentDetails)
admin.site.register(SanctionSetting)
admin.site.register(CommissionSetting)