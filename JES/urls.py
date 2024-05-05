from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path
from asosiy.views import *
from django.conf import settings
from django.conf.urls.static import static
schema_view = get_schema_view(
   openapi.Info(
      title="IshoraAI API",
      default_version='version-1',
      description="Khayitboev Elbekjon || Backend developer and ML engineer \n\nIshora AI uchun API (Version-one)",

      contact=openapi.Contact("Xayitboeyev Elbekjon <backenddevolpment@gmail.com>"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/',schema_view.with_ui('swagger',cache_timeout=0)),
    path('redoc/',schema_view.with_ui('redoc',cache_timeout=0)),
    path('text/',Text.as_view(),name='text'),
    path('gif/',Gif.as_view(),name='gif'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
