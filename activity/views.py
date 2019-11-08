
from django.shortcuts import render
from django.db.models import Q
from accounts.models import User
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.generics import (
    ListAPIView, 
    RetrieveAPIView, 
    ListCreateAPIView,
    DestroyAPIView,
    CreateAPIView,
    UpdateAPIView,
    )

from activity.serializers import (
    CreateActivitySerializer,
    ListActivitySerializer,
    DetailActivitySerializer,
    UpdateActivitySerializer,
    )

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from activity.models import(
    Activity,
)

from rest_framework.parsers import JSONParser,FormParser

''' 
    Activity Calendar API Views
'''
class RequestActivityCreateView(ListCreateAPIView):
    serializer_class = CreateActivitySerializer
    permission_class = [IsAuthenticated]
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = '/careerconsultant/templates/activity_request.html'
    queryset = Activity.objects.all()
    parser_classes = [JSONParser]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status=1)
        
    
def create_activity(request):
    return render(request, 'activity/create_activity.html')


class RequestActivityListView(ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = ListActivitySerializer
    lookup_field = 'pk'


class RequestActivityDetailView(RetrieveAPIView):
    queryset = Activity.objects.all()
    serializer_class = DetailActivitySerializer
    lookup_field = 'pk'
    
class RequestActivityUpdateView(UpdateAPIView):
    queryset = Activity.objects.all()
    serializer_class = UpdateActivitySerializer
    lookup_field = 'pk'
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.cbm_rejected()
        instance.save()
        
      
