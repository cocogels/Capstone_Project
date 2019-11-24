from centermanager.models import SchoolYear
from django.db.models.signals import pre_save
from django.dispatch import receiver




@receiver(pre_save, sender=SchoolYear)
def school_year_save(sender, instance, **kwargs, self):
    active = SchoolYear.objects.get(id=self.id)
  
    if active is None:
        active.active_year = start_year <= end_year
        
        SchoolYear.objects.create(start_year=start_year, end_year=end_year,)
    else:
        SchoolYear.objects.get(id=self.id).update(active_year=False)
        
        active.save(update_fields=[active_year=False])
        
                                                                   