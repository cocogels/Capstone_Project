from django import forms

from registrar.models import RequirementsModel, AvailableCourseModel




class RequirementsForm(forms.ModelForm):
    
    class Meta:
        model = RequirementsModel
        fields = (
            'requirements_name',
            'category',
        )

    def clean_name(self, *args, **kwargs):
        requirements = self.cleaned_data.get('requirements_name')
        queryset = RequirementsModel.objects.filter(requirements_name=requirements)
        if queryset.exists():
            raise forms.ValidationError('This Name Has Already Been used.')
        return requirements




class AvailableCourseForm(forms.ModelForm):
    
    class meta:
        model = AvailableCourseModel
        feilds = (
            'course_name',
            'category',
        )

    def clean_course_name(self, *args, **kwargs):
        course = self.cleaned_data.get('course_name')
        queryset = AvailableCourseModel.objects.filter(course_name=course)
        if queryset.exists():
            raise forms.ValidationError('This Course Name Has Already Been used')
        return course
    
    