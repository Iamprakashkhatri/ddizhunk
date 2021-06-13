from rest_framework import viewsets
from misc import serializers
from django.db import IntegrityError
from django.utils.text import slugify
from django.http import Http404
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .permissions import IsAdminUserOrReadOnly
from .models import SlideShow,FAQ
class SliderViewSet(viewsets.ModelViewSet):
    """ Manage Slider Images 
    ## Fields:
        slider_image, title, active
    ## Filtering Options:
        active
        http://localhost:8000/api/v1/product/slider-images/?active=true

    """
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = SlideShow.objects.all()
    serializer_class = serializers.SlideShowSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['active']
    lookup_field = 'slug'

    def create(self, request):
        serializer = serializers.SlideShowSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            FAIL = True
            slug = slugify(obj.title)
            temp = obj.id
            while FAIL:
                try:
                    obj.slug = slug
                    obj.save()
                    FAIL = False
                except IntegrityError:
                    slug += str(temp)
                    temp += temp

            return Response({'message': 'Successfully Added Slideshow', 'data': serializer.data}, status=201)
        else:
            return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        ss = self.get_object()
        serializer = serializers.SlideShowSerializer(ss, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            FAIL = True
            slug = slugify(obj.title)
            temp = obj.id
            while FAIL:
                try:
                    obj.slug = slug
                    obj.save()
                    FAIL = False
                except IntegrityError:
                    slug += str(temp)
                    temp += temp

            return Response({'message': 'Successfully Edited Slideshow', 'data': serializer.data}, status=201)
        else:
            return Response(serializer.errors, status=400)


    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            name = instance.title
            self.perform_destroy(instance)
        except Http404:
            return Response({'message': 'No Such Content'}, status=404)

        return Response({'message': f'{name} Deleted Successfully'}, status=200)

class FAQViewSet(viewsets.ModelViewSet):
    '''
    Answering the frequently asked questions by users.
    Filtering option is_active
    '''
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = FAQ.objects.all()
    serializer_class = serializers.FAQSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['is_active']
    lookup_field = 'slug'
    def create(self, request):
        serializer = serializers.FAQSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            FAIL = True
            slug = slugify(obj.question)
            temp = obj.id
            while FAIL:
                try:
                    obj.slug = slug
                    obj.save()
                    FAIL=False
                except IntegrityError:
                    slug += str(temp)
                    temp+=temp
            
            return Response({'message': 'Successfully Added FAQ', 'data': serializer.data}, status=201)
        else:
            return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        faq = self.get_object()
        serializer = serializers.FAQSerializer(faq, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            obj = serializer.save()
            FAIL = True
            slug = slugify(obj.question)
            temp = obj.id
            while FAIL:
                try:
                    obj.slug = slug
                    obj.save()
                    FAIL=False
                except IntegrityError:
                    slug += str(temp)
                    temp+=temp

            return Response({'message': 'Successfully Edited FAQ', 'data': serializer.data}, status=201)
        else:
            return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            name = instance.question
            self.perform_destroy(instance)
        except Http404:
            return Response({'message': 'No Such Role'}, status=404)

        return Response({'message': f'{name} Deleted Successfully'}, status=200)
