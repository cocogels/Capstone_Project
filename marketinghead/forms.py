from django import forms

from .models import Budget, Collateral, AssignQuota, AssignTerritory

from accounts.models import Profile, UserMarketingProfile
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
            'unit',
            'quantity',
        )
    
    def clean_title(self, *args, **kwargs):
        collateral = self.cleaned_data.get('c_name')
        qs = TargetSheet.objects.filter(c_name=collateral)
        if qs.exists():
            raise forms.ValidationError('This Name Has Already Been used')
        return collateral
    
    

    

class AssignQuotaForm(forms.ModelForm):
    
    user_profile = forms.ModelChoiceField(queryset=Profile.objects.all(), label='Assign To:')
    
    class Meta:
        model = AssignQuota
        fields = (
            'user_profile',
            'a_senior_high',
            'a_higher_education',
            'a_retail',
            'a_corporate',
            'a_owwa',
        )
        
        labels = {
            'a_senior_high': 'Senior High',
            'a_higher_education': 'Higher Education',
            'a_retail': 'Retail',
            'a_corporate': 'Corporate',
            'a_owwa':'OWWA',
        }

    
    def save(self, commit=True):
        
        user = super(AssignQuotaForm, self).save(commit=False)
        user = AssignQuota(
            user_profile        =self.cleaned_date['user_profile'],
            a_senior_high       =self.cleaned_data['a_senior_high'],
            a_higher_education  =self.cleaned_data['a_higher_education'],
            a_retail            =self.cleaned_data['a_retail'],
            a_corporate         =self.cleaned_data['a_corporate'],
            a_owwa              =self.cleaned_data['a_owwa'],
            
        )
        
        if commit:
            user.save()
        return user


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
