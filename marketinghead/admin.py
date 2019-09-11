from django.contrib import admin
from .models import Budget, Collateral, AssignQuota, AssignTerritory
# Register your models here.





admin.site.register(Budget)
admin.site.register(Collateral)
admin.site.register(AssignQuota)
admin.site.register(AssignTerritory)

