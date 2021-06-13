from rest_framework import serializers
from .models import SlideShow,FAQ

class SlideShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlideShow
        fields = ('id', 'title','slider_image','slider_sub_header','active','slug')
        read_only_fields = ('id', 'slug')

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ('id', 'question', 'answer', 'is_active', 'slug')
        read_only_fields = ('slug', )