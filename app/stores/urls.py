from django.conf.urls import url
from rest_framework import routers

from app.stores.views import BoxViewSet, UserViewSet, MyBoxViewSet

router = routers.SimpleRouter()

urlpatterns = [
    url(r'^user/signup/$', UserViewSet.as_view({'post': 'create'}), name='signup'),
    url(r'^my-box/$', MyBoxViewSet.as_view({'get': 'list'}), name='my-box'),
]
router.register(r'box', BoxViewSet, basename='box')

urlpatterns += router.urls