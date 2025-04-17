from blog.models import Post
from django.core.management.base import BaseCommand
from typing import Any
from blog.models import Category

class Command(BaseCommand):
    help='inserting data'
    
    

    def handle(self, *args:Any, **options:Any):
        Category.objects.all().delete()
        categories=['Science','Entertainment','Food','Sports','Topper']
        for category_name in categories:
            Category.objects.create(name=category_name)
            
        self.stdout.write(self.style.SUCCESS("completed inserting data"))