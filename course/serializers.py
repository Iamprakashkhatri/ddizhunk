from rest_framework import serializers
from account.serializers import BasicOwnerSerializer
from course.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['slug', ]

class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
                    queryset=Category.objects.all())
    category_title = serializers.CharField(source='category.title', read_only=True)
    class Meta:
        model = SubCategory
        fields = ['id','category','category_title','title','slug','status','no_of_hours','no_of_lessons','thumbnail']
        read_only_fields = ['slug','category','category_title']

class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Course
        fields =['id','category','title','overview','created','description','price','preview_video','sale_price']
        # fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ['id','order', 'title', 'description', 'contents', 'time']

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Module
        fields = '__all__'

class CourseContentSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True)
    no_of_lessons = serializers.IntegerField(required=False, allow_null=True)
    no_of_topics = serializers.IntegerField(required=False, allow_null=True)
    no_of_enroll = serializers.IntegerField(required=False, allow_null=True)
    sub_category = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all())
    sub_cat_title = serializers.CharField(source='sub_category.title', read_only=True)
    category_title = serializers.CharField(source='sub_category.category.title', read_only=True)
    category_id = serializers.CharField(source='sub_category.category.id', read_only=True)
    rating = serializers.IntegerField(required=False)
    owner = BasicOwnerSerializer(many=True,read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'sub_category','sub_cat_title', 'category_title',
                  'category_id', 'title', 'slug', 'overview',
                  'created', 'owner', 'modules', 'price', 'sale_price',
                  'description', 'thumbnail', 'preview_video', 'no_of_lessons',
                  'no_of_topics', 'no_of_enroll', 'rating',
                  'syllabus','notes'
                  ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")

        if instance.students.filter(id=request.user.id).exists():
            representation['enrolled'] = True
            representation['main_category'] = None
            if instance.sub_category:
                representation['main_category'] = instance.sub_category.category.title
        else:
            representation['enrolled'] = False
            representation['main_category'] = None
            if instance.sub_category:
                representation['main_category'] = instance.sub_category.category.title
        return representation


class LessonWithContentsCreateSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, required=False)

    class Meta:
        model = Lesson
        exclude = ['module', ]


class ModuleWithLessonsCreateSerializer(serializers.ModelSerializer):
    lessons = LessonWithContentsCreateSerializer(many=True, required=False)

    class Meta:
        model = Module
        exclude = ['course', ]


class CourseGetSerializer(serializers.ModelSerializer):
    modules = ModuleWithLessonsCreateSerializer(many=True, required=False)
    class Meta:
        model = Course
        fields = '__all__'

class CourseCreateSerializer(serializers.ModelSerializer):
    modules = ModuleWithLessonsCreateSerializer(many=True, required=False)

    class Meta:
        model = Course
        exclude = ['owner', 'slug', 'students', ]

    def create(self, validated_data):
        modules = validated_data.pop('modules')
        request = self.context.get("request")
        print('request',request)
        if request and hasattr(request, "user"):
            course = Course.objects.create(**validated_data)
            print('course',cou)
            course.owner.add(request.user)
            print('course',course.owner.add(request.user))
            course.save()
            for module in modules:
                lessons = module.pop('lessons')
                created_module = Module.objects.create(course=course, **module)
                for lesson in lessons:
                    contents = lesson.pop('contents')
                    created_lesson = Lesson.objects.create(module=created_module, **lesson)
                    for content in contents:
                        Content.objects.create(lesson=created_lesson, **content)
            return self.data
        else:
            raise serializers.ValidationError("Server error,User unknown.")


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class UpdateCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'

class UpdateModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = '__all__'


class UpdateLessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class UpdateContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = '__all__'





