from django.db import models
from accounts.models import User
from django_fsm import FSMField, transition, FSMIntegerField
import arrow
from django.utils.translation import gettext, gettext_lazy as _






    
class Activity(models.Model):
    STATUS_CREATED  = 0
    PENDING_1       = 1
    APPROVED_1      = 2
    REVISED_1       = 3
    PENDING_2       = 4
    APPROVED_2      = 5
    REVISED_2       = 6
    PENDING_3       = 7
    APPROVED_3      = 8
    REVISED_3       = 9    
    REJECTED        = 10
    CANCELLED       = 11

    STATUS_CHOICES = (
        (STATUS_CREATED, 'created'),
        (PENDING_1, 'pending 1 '),
        (APPROVED_1, 'apppoved 1'),
        (REVISED_1, 'revised 1'),
        (PENDING_2, 'pending 2'),
        (APPROVED_2, 'apppoved 2'),
        (REVISED_2, 'revised 2'),
        (PENDING_3, 'pending 3'),
        (APPROVED_3, 'apppoved 3'),
        (REVISED_3, 'revised 3'),
        (REJECTED, 'rejected'),
        (CANCELLED, 'cancelled'),
    )

    activity_id     = models.AutoField(primary_key=True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE,)
    start_date      = models.DateTimeField(null=False, blank=False)
    end_date        = models.DateTimeField(null=False, blank=False)
    activity_name   = models.CharField(max_length=100)
    location        = models.CharField(max_length=150)
    description     = models.TextField(max_length=255)
    comment         = models.TextField(max_length=255, blank=True)
    #BUDGET
    #COLLATERAL
    status = FSMIntegerField(choices=STATUS_CHOICES, default=STATUS_CREATED, protected=True)
    date_created    = models.DateTimeField(_('Date Created'), auto_now_add=True)
    date_updated    = models.DateTimeField(_("Date Updated"), auto_now=True)
    
    
    def __str__(self):
        return self.activity_name

    def created_on_arrow(self):
        return arrow.get(self.date_created).humanize()
    
    def updated_on_arrow(self):
        return arrow.get(self.date_updated).humanize()
    
    @transition(field=status, source=[STATUS_CREATED], target=PENDING_1)
    def cbm_pending(self):
        self.user = self.user
        self.activity_name = self.activity_name
        self.start_date = self.start_date
        self.end_date   = self.end_date
        self.location = self.location
        self.description = self.description
        #COLLATERAL
        #BUDGET
        print("Requested Activity {} Pending!".format(self.activity_name))
    
    @transition(field=status, source=[PENDING_1], target=CANCELLED)
    def cancel(self):
        self.activity_name = activity_name
        self.start_date = start_date
        self.end_date = end_date
        self.location = location
        self.description = description
        #COLLATERAL
        #BUDGET
        print('Requested Activity {} Cancelled'.format(self.activity_name))
    
    
    
    
    @transition(field=status, source=[PENDING_1], target=REVISED_1)
    def cbm_revised(self):
        self.user = self.user
        self.activity_name = self.activity_name
        self.start_date = self.start_date   
        self.end_date = self.end_date
        self.location = self.location
        self.description = self.description
        self.comment = self.comment
        #COLLATERAL
        #BUDGET
        
        print("Requested Activity {} Revised!".format(self.activity_name))
    
    @transition(field=status, source=[REVISED_1], target=PENDING_1)
    def cbm_revised_complete(self):
        self.user = self.user
        self.activity_name = self.activity_name 
        self.start_date = self.start_date
        self.end_date = self.end_date
        self.location = self.location
        self.description = self.description
        #Collateral
        #Budget
        print("Revised Activity {} ".format(self.activity_name))
            
    @transition(field=status, source=[PENDING_1], target=REJECTED)
    def cbm_rejected(self):
        self.user = self.user
        self.activity_name = self.activity_name
        self.start_date = self.start_date
        self.end_date = self.end_date
        self.location = self.location
        self.description = self.description
        self.comment = self.comment
        #COLLATERAL
        #Budget
        print('Requested Activtity {}'.format(self.activity_name))
        
        
    @transition(field=status, source=[PENDING_1], target=APPROVED_1)
    def cbm_approved(self):
        self.user = self.user
        self.activity_name = self.activity_name
        self.start_date = self.start_date
        self.end_date = self.end_date
        self.location = self.location
        self.description = self.description
        #Collateral
        #Budget
        print("Requested Activity {} Approved!".format(self.activity_name))
    
    @transition(field=status, source=[APPROVED_1], target=PENDING_2)
    def cbm_approved_transfer(self):    
        self.user = self.user
        self.activity_name = self.activity_name
        self.start_date = self.start_date
        self.end_date = self.end_date
        self.location = self.location
        self.description = self.desciption
        #Collateral
        #Budget
        print('Approved Activity {} Transfer'.format(self.activity_name))
    
    '''
    MH FLOW TO BE FOLLOWED
    '''
    class Meta:
        verbose_name = _('Activity Request')
        verbose_name_plural = _('Activity Requests')


