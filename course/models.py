from django.db import models
from account.models import User
from django.template.defaultfilters import slugify
from .fields import OrderField


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    status = models.CharField(max_length=200, default='')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(__class__, self).save(*args, **kwargs)


class SubCategory(models.Model):
    category = models.ForeignKey(Category,related_name='rel_category', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    status = models.CharField(max_length=200, default='')
    no_of_hours = models.IntegerField(default=0)
    no_of_lessons = models.IntegerField(default=0)
    thumbnail = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(__class__, self).save(*args, **kwargs)


class Course(models.Model):
    owner = models.ManyToManyField(User, related_name='teacher')
    sub_category = models.ForeignKey(SubCategory, related_name='rel_sub_category', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)
    description = models.TextField(default='')
    syllabus = models.TextField(default='')
    notes = models.TextField(default='')
    price = models.IntegerField(default=0)
    preview_video = models.URLField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    sale_price = models.IntegerField(default=0)
    visibility = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + str(self.id)
        super(__class__, self).save(*args, **kwargs)


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order']


class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['module'])
    video = models.URLField(null=True, blank=True)
    time = models.CharField(max_length=300, null=True, blank=True, default='0')

    def __str__(self):
        return f'{self.order}. {self.title}'

    def save(self, *args, **kwargs):
        if self.video:
            clip = VideoFileClip('{name}'.format(name=self.video))
    
            self.time = clip.duration
        super(Lesson, self).save(*args, **kwargs)


    class Meta:
        ordering = ['order']


class Content(models.Model):
    title = models.CharField(max_length=250, default='')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    lesson = models.ForeignKey(Lesson, related_name='contents', on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.CharField(max_length=10, choices=(
        ('Video', 'Video'),
        ('Text', 'Text'),
        ('File', 'File')
    ), default='Video')
    text = models.TextField(default='')
    video = models.URLField(default="https://cdn.padhaisewa.com")
    file = models.FileField(upload_to='files', blank=True, null=True)
    time = models.CharField(max_length=300, blank=True, null=True, default='0')
    order = OrderField(blank=True, for_fields=['lesson'])
    
    def __str__(self):
        return self.title


class FileUpload(models.Model):
    video = models.FileField(upload_to='files/')
    title = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.title

class Rating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings')
    text = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating_user')

    def __str__(self):
        return self.text