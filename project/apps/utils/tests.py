from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from user.models import User
from user.serializers import SignUpSerializer
from user.serializers import CustomTokenObtainPairSerializer
from tenants.models import Client

class BaseSetup(TenantTestCase):
    
    def setUp(self):
        super().setUp()
        self.c = TenantClient(self.tenant)
        self.set_user_data()
        self.headers =  {"HTTP_AUTHORIZATION" : f"Bearer {str(self.user_data['access'])}", "content_type" :'application/json'}

    @staticmethod
    def generate_custom_user_token(user):
        user_data = CustomTokenObtainPairSerializer.get_token(user)
        return {"HTTP_AUTHORIZATION" : f"Bearer {str(user_data.access_token)}", "content_type" :'application/json'}

    @classmethod
    def setup_tenant(cls, tenant : Client):
        return tenant
        

    def set_user_data(self):
        self.user = User.objects.create_superuser('mohamed_naser', **{
            "first_name": "mohamed",
            "last_name": "naser",
            "email": "mn9142001@gmail.com",
            "password": "Mohamed13#",
        })
        
        self.user_data = SignUpSerializer(instance=User.objects.first()).data
