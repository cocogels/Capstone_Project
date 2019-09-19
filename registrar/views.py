from django.shortcuts import render

# Create your views here.


def available_course_view(request):
    template_name = 'available_course/available_course_details.html'
    return render(request, template_name)



def student_requirements_view(request):
    template_name = 'stud_requirements/student_requirements_details.html'
    return render(request, template_name)

# def create_collateral(request):
#     if request.method == 'POST':
#         form = CollateralForm(request.POST)

#         if form.is_valid():

#              unit     = form.cleaned_data['unit']
#              quantity = form.cleaned_data['quantity']

#         create = Collateral(
#             unit=unit,
#             quantity=quantity,
#         )

#         create.save()
#         messages.success(request, 'You Have Successfully Added Collateral Details')
#         return redirect('marketing_head:collateral_list')

#     else:
#         form = CollateralForm()

#     template_name = 'collateral/create_collateral.html'
#     context = {
#         'form': form
#     }

#     return render(request, template_name, context)


# class CollateralListView(ListView):
#     model = Collateral
#     template_name = 'collateral/collateral_list.html'
#     queryset = Collateral.objects.all()


# class CollateralDetailView(DetailView):
#     model = Collateral
#     template_name = 'collateral/collateral_detail.html'


# class CollateralUpdateView(UpdateView):
#     model = Collateral
#     template_name = 'collateral/create_collateral.html'
#     form_class = CollateralForm
#     success_url = reverse_lazy('marketing_head:collateral_list')

#     def form_valid(self, form):
#         form.save()
#         messages_text = 'Your {} was Updated Successfully!'.format(
#             form.instance)
#         messages.success(self.request, message_text)
#         if 'continue' in self.request.POST:
#             return HttpResponseRedirect(
#                 reverse_lazy(
#                     'marketing_head:collateral_update',
#                     kwargs={'pk': form.instance.pk}
#                 )
#             )

#         else:
#             return super().form_valid(form)


