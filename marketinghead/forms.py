from django import forms

from .models import Budget, Collateral, AssignQuota, AssignTerritory

from accounts.models import Profile, User
from bootstrap_datepicker_plus import MonthPickerInput
# class AssignIHEForm(forms.ModelForm):
    
#     class Meta:
#         model = AssignIHE
#         fields = ['a_senior_high', 'a_higher_education']


# class AssignICLForm(forms.ModelForm):
    
#     class Meta:
#         model = AssignICL
#         fields = ['a_retail','a_corporate','a_owwa']



class BudgetForm(forms.ModelForm):
    

    amount = forms.CharField( label='Budget Amount', widget=forms.NumberInput(),)
    arrival  = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label='Arrival')
    class Meta:
        model   = Budget
        fields  = (
            'amount',
            'arrival',
        ) 
        
        
        
    

class CollateralForm(forms.ModelForm):
    
    class Meta:
        model  = Collateral
        fields = (
            'name',
            'unit',
            'quantity',
        )
    
        labels = {
            'name' : 'Collateral Name',
            'unit' : 'Unit',
            'quantity' : 'Quantity'
                }
    def clean_title(self, *args, **kwargs):
        collateral = self.cleaned_data.get('name')
        qs = TargetSheet.objects.filter(name=collateral)
        if qs.exists():
            raise forms.ValidationError('This Name Has Already Been used')
        return collateral
    
    
def present_or_future_date(value):
    if value < datetime.date.today():
        raise forms.ValidationError("The date cannot be in the past!")
    return value


class AssignQuotaForm(forms.ModelForm):

    

    def __init__(self, *args, **kwargs):
        assigned_users = kwargs.pop('assigned_to',[])
        super(AssignQuotaForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {'class': "form-control"}
        
        if assigned_users:
            self.fields['assigned_to'].queryset = assigned_users
        self.fields['assigned_to'].required = True
        
    class Meta:
        model = AssignQuota
        fields = (
            'assigned_to',
            'start_month',
            'end_month',
            'a_senior_high',
            'a_higher_education',
            'a_retail',
            'a_corporate',
            'a_owwa',
        )
        
        labels = {
            'assigned_to': 'Assign To',
            'a_senior_high': 'Senior High',
            'a_higher_education': 'Higher Education',
            'a_retail': 'Retail',
            'a_corporate': 'Corporate',
            'a_owwa':'OWWA',
        }

        widgets ={
            'start_month': MonthPickerInput().start_of('Assign Quota'),
            'end_month': MonthPickerInput().end_of('Assign Quota'),
        }
        validators = {
           ' start_month':[present_or_future_date],
            'end_month':[present_or_future_date],
        }
        
    def clean(self):
        cleaned_data = super(AssignQuotaForm, self).clean()
        start_month = cleaned_data.get("start_month")
        end_month = cleaned_data.get("end_month")

        if start_month and end_month:
            if start_month > end_month:
                    raise forms.ValidationE('Please Enter A Valid Date')


class AssignTerritoryForm(forms.ModelForm):
    
    user_profile = forms.ModelChoiceField(queryset=Profile.objects.all(), label='Assign To:')
    
    class Meta:
        model = AssignTerritory
        fields = (
            'user_profile',
            'territory_choices',
        )
    
    def save(self, commit=True):
        
        user = super(AssignTerritoryForm, self).save(commit=False)
        user = AssignQuota(
            user_profile        = self.cleaned_date['user_profile'],
            territory_choices   = self.cleaned_data['territory_choices'] ,
        
        )
        if commit:
            user.save()
        return user
#----------------------------------

