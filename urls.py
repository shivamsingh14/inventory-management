from django.conf.urls import url
from rest_framework import routers

from app.stores.views import BoxViewSet

router = routers.SimpleRouter()

urlpatterns = []
router.register(r'box', BoxViewSet, basename='box')

urlpatterns += router.urls
