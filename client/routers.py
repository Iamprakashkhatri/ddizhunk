from rest_framework.routers import DefaultRouter

from client.viewsets.ClientManagement import ClientMyChoiceAPI

router = DefaultRouter()
router.register('client-my-choice', ClientMyChoiceAPI,basename='client-my-choice'),
