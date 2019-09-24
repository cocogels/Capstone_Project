from django import forms 
from contacts.models import ICL_ContactModel



''' Contact Form '''

class ICLContactForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        assigned_users = kwargs.pop('assigned_to', [])
        super(ICLContactForm, self).__init__(*args, **kwargs)
        
        if assigned_users:
            self.fields['assigned_to'].queryset = assigned_users
        self.fields['assigned_to'].required = False
        
       

    class Meta:
        model = ICL_ContactModel
        fields = (
            'assigned_to',
            'name',
            'org_type',
            'tel_number',
            'phone_number',
            'email',
            'person',
            'address',
        )



