from django.shortcuts import render

# Create your views here.


def available_course_view(request):
    template_name = 'available_course/available_course_details.html'
    return render(request, template_name)



def student_requirements_view(request):
    template_name = 'stud_requirements/student_requirements_details.html'
    return render(request, template_name)

