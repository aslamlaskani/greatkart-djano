from django.contrib import admin
from django.urls import path, include  # ✅ include added
from.import views
from django.conf import settings
from django.conf.urls.static import static



 # ✅ views from store app  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # home page
    path('store/', include('store.urls')),  # store app URLs
    
]

# ✅ for serving media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
