from django import forms
from .models import IHE_ContactModel, ICL_ContactModel, SHS_ContactModel, IHE_ContactCategoryModel, ICL_ContactCategoryModel, SHS_ContactCategoryModel


class ICLContactForm(forms.ModelForm):

    email           = forms.EmailField(max_length=255, required=False)
    phone_number    = forms.CharField(max_length=12, widget=forms.NumberInput(), label='Cellphone Number', required=False)
    c_person        = forms.CharField(label='Contact Person', required=True)
    class Meta:
        model = ICL_ContactModel
        fields = (
            'name',
            'org_type',
            'telephone_number',
            'phone_number',
            'email',
            'c_person',
        )


class SHSContactForm(forms.ModelForm):
    
    email           = forms.EmailField(max_length=255, required=False)
    phone_number    = forms.CharField(max_length=12, widget=forms.NumberInput(), label='Cellphone Number', required=False)
    c_person        = forms.CharField(label='Contact Person', required=True)
    class Meta:
        model = SHS_ContactModel
        fields = (
            'name',
            'org_type',
            'c_number_tel',
            'c_number_cp',
            'email',
            'c_person',
        )


class IHEContactForm(forms.ModelForm):

    email = forms.EmailField(max_length=255, required=False)
    phone_number = forms.CharField(max_length=12, widget=forms.NumberInput(), label='Cellphone Number', required=False)
    c_person = forms.CharField(label='Contact Person', required=True)

    class Meta:
        model = IHE_ContactModel
        fields = (
            'name',
            'org_type',
            'c_number_tel',
            'c_number_cp',
            'email',
            'c_person',
        )

    
        
    
    
    # def __init__(self, *args, **kwargs):
        
    #     account_view = kwargs.pop('account', False)
        
    #     super(ICLContactForm,self).__init__(*args,**kwargs)
        
    #     for field in self.fields.values():
    #         field.widget.attrs = {
    #             "class": "form-control"
    #         }
            
    #         self.fields['name'].widget.attrs.update({
                
    #             'placeholder': 'Organization Name'
    #         }
    #         )
            
    #         self.fields['org_type'].choices =[
    #             ('','-------'),] + list(
    #                 self.fields['org_type'.choices][1:]
    #             ) 
            
    #         for key, value in self.fields.items():
                
    #             if key == 'phone_number':
    #                 value.widget.attrs['placeholder'] = "+63-123-456-7890"
    #             else:
    #                 value.widget.attrs['placeholder'] = value.label
            
    #         self.fields['c_person'].widget.attrs.update({'placeholder': 'Contact Person'})
    #         self.fields['email'].widget.attrs.update({'placeholder': 'Enter @email.com '})
    #         self.fields['category'].choices = [(category.get('id'), category('name'))
    #             for category in ICL_ContactCategoryModel.objects.all().values('id','name')
    #         ]
            
    #     if account_view:
    #         self.fields['name'].required=True
    #         self.field['org_type'].required=True
    #         self.field['phone_number'].required=False 
    #         self.field['email'].required=False 
    #         self.field['c_person'].required=True
            

                            
                
            
            #self/fields['telephone_number'].widget.attrs.update('placeholder': 'Organization Name')
        
    def clean_name(self, *args, **kwargs):
        name = self.cleaned_data.get('name')
        query_set = ICL_ContactCategoryModel.objects.filter(name__iexact=name)
        if query_set.exists():
            raise forms.ValidationError('This Name Already Registered..!!')
        return name

        
    def save(self,commit=True):
        
        user = super(ICLContactForm, self).save(commit=False)
        user = ICL_ContactModel( 
            name            = self.cleaned_data['name'],
            org_type        = self.cleaned_data['org_type'],
            telephone_number= self.cleaned_data['telephone_number'],                
            phone_number    = self.cleaned_data['phone_number'],
            email           = self.cleaned_data['email'],
            c_person        = self.cleaned_data['c_person'],
        )
        if commit:
            user.save()
        return user 
    
    
# class IHE_ContactForm(forms.ModelFormm):
#     email           = forms.EmailField(max_length=255, required=False)
#     ihe_name        = forms.CharField()    
#     class Meta:
#         model = IHE_ContactModel
#         fields = (
            
#         )
