from django.db import models
from django.utils.text import slugify
from django.db import IntegrityError


class SlideShow(models.Model):
    slider_image = models.ImageField(upload_to='images/slide-show')
    title = models.CharField(max_length=255, unique=True)
    slider_sub_header = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(default="", max_length=255, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
        
class FAQ(models.Model):
    question = models.CharField(max_length=200, unique=True)
    answer = models.TextField()
    slug = models.SlugField(max_length=255, default="", unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question