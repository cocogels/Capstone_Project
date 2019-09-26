from django import forms 
from contacts.models import ICL_ContactModel, SHS_ContactModel, IHE_ContactModel



''' Contact Form '''

class ICLContactForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        assigned_users = kwargs.pop('assigned_to', [])
        super(ICLContactForm, self).__init__(*args, **kwargs)
        
        if assigned_users:
            self.fields['assigned_to'].queryset = assigned_users
        self.fields['assigned_to'].required = False
        
        self.fields['name'].widget.attrs['placeholder'] = 'Organization Name'
        self.fields['tel_num_digits'].widget.attrs['placeholder'] = '000'
        self.fields['tel_num'].widget.attrs['placeholder'] = '0000'
        self.fields['phone_number'].widget.attrs['placeholder'] = '1234567890'
        self.fields['email'].widget.attrs['placeholder'] = '@email.com'
        self.fields['person'].widget.attrs['placeholder'] = 'Contact Person'
        self.fields['address'].widget.attrs['placeholder'] = 'Organization Address'


        self.fields['tel_area'].widget.attrs['size']='1'
        self.fields['tel_num_digits'].widget.attrs['size'] = '1'
        self.fields['tel_num'].widget.attrs['size'] = '2'

    class Meta:
        model = ICL_ContactModel
        fields = (
            'assigned_to',
            'name',
            'org_type',
            'tel_area',
            'tel_num_digits',
            'tel_num',
            'phone_number',
            'email',
            'person',
            'address',
        )


class SHSContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        assigned_users = kwargs.pop('assigned_to', [])
        super(SHSContactForm, self).__init__(*args, **kwargs)

        if assigned_users:
            self.fields['assigned_to'].queryset = assigned_users
        self.fields['assigned_to'].required = False

        self.fields['name'].widget.attrs['placeholder'] = 'Organization Name'
        self.fields['tel_num_digits'].widget.attrs['placeholder'] = '000'
        self.fields['tel_num'].widget.attrs['placeholder'] = '0000'
        self.fields['phone_number'].widget.attrs['placeholder'] = '1234567890'
        self.fields['email'].widget.attrs['placeholder'] = '@email.com'
        self.fields['person'].widget.attrs['placeholder'] = 'Contact Person'
        self.fields['address'].widget.attrs['placeholder'] = 'Organization Address'

        self.fields['tel_area'].widget.attrs['size'] = '1'
        self.fields['tel_num_digits'].widget.attrs['size'] = '1'
        self.fields['tel_num'].widget.attrs['size'] = '2'

    class Meta:
        model = SHS_ContactModel
        fields = (
            'assigned_to',
            'name',
            'org_type',
            'tel_area',
            'tel_num_digits',
            'tel_num',
            'phone_number',
            'email',
            'person',
            'address',
        )






class IHEContactForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        assigned_users = kwargs.pop('assigned_to', [])
        super(IHEContactForm, self).__init__(*args, **kwargs)

        if assigned_users:
            self.fields['assigned_to'].queryset = assigned_users
        self.fields['assigned_to'].required = False

        self.fields['name'].widget.attrs['placeholder'] = 'Organization Name'
        self.fields['tel_num_digits'].widget.attrs['placeholder'] = '000'
        self.fields['tel_num'].widget.attrs['placeholder'] = '0000'
        self.fields['phone_number'].widget.attrs['placeholder'] = '1234567890'
        self.fields['email'].widget.attrs['placeholder'] = '@email.com'
        self.fields['person'].widget.attrs['placeholder'] = 'Contact Person'
        self.fields['address'].widget.attrs['placeholder'] = 'Organization Address'

        self.fields['tel_area'].widget.attrs['size'] = '1'
        self.fields['tel_num_digits'].widget.attrs['size'] = '1'
        self.fields['tel_num'].widget.attrs['size'] = '2'

    class Meta:
        model = IHE_ContactModel
        fields = (
            'assigned_to',
            'name',
            'org_type',
            'tel_area',
            'tel_num_digits',
            'tel_num',
            'phone_number',
            'email',
            'person',
            'address',
        )
