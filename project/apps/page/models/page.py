from django.db import models

class Page(models.Model):
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    page_content = models.CharField(max_length=10240)
    
    