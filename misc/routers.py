from rest_framework.routers import DefaultRouter

from misc import viewsets

router = DefaultRouter()
router.register('slider-images', viewsets.SliderViewSet)
router.register('faq', viewsets.FAQViewSet)
