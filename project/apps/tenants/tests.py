from utils.tests import BaseSetup
from user.models import User
from django.conf import settings

# Create your tests here.

class TenantTest(BaseSetup):
    
    def test_get_currency(self):
        response = self.c.get(f'/tenants/currency', **self.headers, follow=True)
        assert response.status_code < 400, response.content
        
    @property
    def tenant_handler_user(self):
        return User.objects.get_or_create(username=settings.TENANT_HANDLER_USERNAME, password="reallyDummyText")[0]