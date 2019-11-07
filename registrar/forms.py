from django import forms

from registrar.models import (
    RequirementsModel,
    RequirementsTransfereeModel,
    CourseModel,
)




class RequirementsForm(forms.ModelForm):
    class Meta:
        model = RequirementsModel
        fields = (
            'requirements_name',
        )
        
    def clean_requirements_name(self):
        requirements = self.cleaned_data.get('requirements_name')
        queryset = RequirementsModel.objects.filter(requirements_name=requirements)
        if queryset.exists():
            raise forms.ValidationError('This {} Has Already Been Used'.format(self.requirements_name))
        return requirements
    

class RequirementsTransfereeForm(forms.ModelForm):
    
    class Meta:
        model = RequirementsTransfereeModel
        fields= (
            'requirements_name',
        )
    
    # def clean_requirements_name(self):
    #     requirements = self.cleaned_data.get('requirements_name')
    #     queryset = RequirementsModel.objects.filter(requirements_name=requirements)
    #     if queryset.exists():
    #         raise forms.ValidationError('This {} Has Already Been Used'.format(self.requirements_name ))
    #     return requirements
    


class CourseForm(forms.ModelForm):
    class Meta:
        model = CourseModel
        fields = (
            'course_name',
            'course_description',
        )

    # def clean_course_name(self):
    #     course   = self.cleaned_data.get('course_name')
    #     queryset = CourseModel.objects.filter(course_name=course)
    #     if queryset.exists():
    #         raise forms.ValidationError('This {} Has Alteady Been Used'.format(self.course_name) )
    
    
