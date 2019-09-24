from django.db import models
import arrow 
from django.utils.translation import ugettext_lazy as _
from category.models import ICL_ContactCategoryModel, SHS_ContactCategoryModel, IHE_ContactCategoryModel
from accounts.models import User
from django.core.validators import RegexValidator
''' ICL CONTACTS '''

class ICL_ContactModel(models.Model):
    
    name        = models.CharField(max_length=100)
    assigned_to = models.ManyToManyField(User, related_name='contact_assigned_user')
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cotact_created_by')
    org_type    = models.ForeignKey(ICL_ContactCategoryModel, on_delete=models.CASCADE)
    tel_regex   = RegexValidator(regex=r'\d{7}$', message='Telephone Number is up to 7 digits allowed' )
    tel_number  = models.CharField(validators=[tel_regex] , max_length=7,blank=True, null=True, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Phone Number must entered in the format:'+123456789'.Up to 12 digits allowed.")
    phone_number= models.CharField(validators=[phone_regex],max_length=12, null=True, blank=True, unique=True)
    email       = models.EmailField(max_length=100)
    person      = models.CharField(max_length=100)
    address     = models.CharField(max_length=255)
    is_active   = models.BooleanField(default=False)
    date_created= models.DateTimeField(_('Date Created'), auto_now_add=True)
    date_updated= models.DateField(auto_now=True)
    
    @property
    def __str__(self):
        return self.name
    
    def created_on_arrow(self):
        return arrow.get(self.date_created).humanize()
    
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()
    
    def date_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date_created <= now

    class Meta:
        ordering = ('-date_created',)
        verbose_name        = 'ICL Contact Detail'
        verbose_name_plural = 'ICL Contact Details'
