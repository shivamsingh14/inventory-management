from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('', include('app.stores.urls'), name='store'),
]
