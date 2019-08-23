from django.test import TestCase
from .models import UserMarketingProfile SimpleTestCase 
# Create your tests here.


class UserMarketingProfileTest(TestCase):
    
    def test_empty_string_as_centermanager(self):
        UserMarketingProfile(centermanager='').save()