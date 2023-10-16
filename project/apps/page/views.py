from rest_framework.viewsets import ModelViewSet
from .models import Page
from .serializers import PageSerializer

class PageViewSet(ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    authentication_classes = []
    permission_classes = []