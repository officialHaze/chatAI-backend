from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os
from dotenv import load_dotenv

load_dotenv()

urlpatterns = [
    path(f'admin/{os.environ.get("ADMIN_SECRET")}/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf'))
]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)