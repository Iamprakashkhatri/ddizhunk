from rest_framework.routers import DefaultRouter

from account.views import NewsletterViewset

router = DefaultRouter()
router.register('newsletter', NewsletterViewset,basename='news-letter'),
