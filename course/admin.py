from django.contrib import admin
from course.models import (
    Course, Category, SubCategory,
    Module, Lesson,Content,Rating,
    FileUpload
    )

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Content)
admin.site.register(Rating)
admin.site.register(FileUpload)
