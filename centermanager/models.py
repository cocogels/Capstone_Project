from django.db import models
from django.utils import timezone

# Create your models here.


class TargetSheet(models.Model):

    ts_id           = models.AutoField(primary_key=True)
    start_year      = models.DateField(blank=True, null=True)
    end_year        = models.DateField(blank=True, null=True)
    corporate       = models.BigIntegerField(null=True,)
    retail          = models.BigIntegerField(null=True,)
    owwa            = models.BigIntegerField(null=True,)
    seniorhigh      = models.BigIntegerField(null=True,)
    higher_ed       = models.BigIntegerField(null=True,)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)
    
    def date_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_added <= now
    
    class Meta:
        verbose_name_plural = 'Target Sheet'



class PaymentDetails(models.Model):
    status_choices =(
        ('regular', 'RegularClass'),
        ('nightclass', 'NightClass')
    )
    status = models.CharField(
        max_length=50,
        choices=status_choices,
        default='regular'
    )
    payment_details_id      = models.AutoField(primary_key=True)
    cash_amount_per_unit    = models.BigIntegerField(null=True)
    cash_miscellaneous_fee  = models.BigIntegerField(null=True)
    cash_lab_fee            = models.BigIntegerField(null=True)
    cash_registration_fee   = models.BigIntegerField(null=True)
    ins_amount_unit         = models.BigIntegerField(null=True)
    ins_miscellaneous_fee   = models.BigIntegerField(null=True)
    ins_lab_fee             = models.BigIntegerField(null=True)
    ins_registration_fee    = models.BigIntegerField(null=True)
    date_created            = models.DateTimeField(auto_now_add=True)
    date_updated            = models.DateTimeField(auto_now=True)

    
    
    def __str__(self):
        return self.status
    
    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now


    class Meta:
        verbose_name_plural ='Payment Details'
        
        





class SanctionSetting(models.Model):
    ss_id           = models.AutoField(primary_key=True)
    first_sanction  = models.CharField(max_length=255, blank=False)
    second_sanction = models.CharField(max_length=255, blank=False)
    third_sanction  = models.CharField(max_length=255, blank=False)
    fourth_sanction = models.CharField(max_length=255, blank=False)
    fifth_sanction  = models.CharField(max_length=255, blank=False)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_updated    = models.DateTimeField(auto_now=True)
    
    def date_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_added <= now
    
    class Meta:
        verbose_name_plural ='Sanction Settings'
        
    


# def valid_pct(val):
#     if val.endwith("%"):
#         return float(val[:-1])/100
#     else:
#         try:
#             return float(val)
#         except ValueError:
#             raise ValidationError(
#                 _('%(value)s is not a valid pct'),
#                 params={'value': value},
#             )
class CommissionSetting(models.Model):
    fee_choices     = (
                    (True, 'PAID'), 
                    (False ,'UNPAID'),
                    )
    stud_choices    = (
                    (True, 'ENROLLED'), 
                    (False,'DROP'), 
                    )
    
    
    cs_id              = models.AutoField(primary_key=True)
    tuition_percentage = models.SmallIntegerField(null=True)
    misc_fee_status    = models.BooleanField(choices=fee_choices,)
    reg_fee_status     = models.BooleanField(choices=fee_choices,)
    stud_fee_status    = models.BooleanField(choices=stud_choices,)
    date_created       = models.DateTimeField(auto_now_add=True)
    date_updated       = models.DateTimeField(auto_now=True)
    
    
    def date_added_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_added <= now
    
    class Meta:
        
        verbose_name_plural = 'Commission Settings'
