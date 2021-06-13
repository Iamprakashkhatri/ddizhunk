from rest_framework import serializers
from account.models import User
from course.models import Course,Category,SubCategory
from course.serializers import CategorySerializer
class SubcategorySerializer(serializers.ModelSerializer):
    no_of_enroll = serializers.IntegerField(required=False, allow_null=True)
    total_sales = serializers.IntegerField(required=False,allow_null=True)
    rating = serializers.IntegerField(required=False,allow_null=True)
    class Meta:
        model = SubCategory
        fields = ['id','title','no_of_enroll','total_sales','rating']

class AccountCategorySerializer(serializers.ModelSerializer):
    # category1=CategorySerializer(many=True,source='sub_category')
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),source='sub_category')
    sub_category = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all())
    sub_cat_title = serializers.CharField(source='sub_category.title', read_only=True)
    category_title = serializers.CharField(source='sub_category.category.title', read_only=True)
    category_id = serializers.CharField(source='sub_category.category.id', read_only=True)
    no_of_enroll = serializers.IntegerField(required=False, allow_null=True)
    total_sales = serializers.IntegerField(required=False,allow_null=True)
    payment_mode = serializers.CharField(required=True,allow_null=True)
    rating = serializers.IntegerField(required=True,allow_null=True)
    class Meta:
        model = Course
        fields = ['id','title','sub_category','sub_cat_title','category_title','category_id','no_of_enroll','total_sales','payment_mode','rating']

class AccountTeacherSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(required=False, allow_null=True)
    # viewers = serializers.IntegerField(required=False,allow_null=True)
    class Meta:
        model = User
        fields = ['id','first_name','last_name','course_name']