
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tracker import views as tracker_views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tracker_views.home, name='home'),
    path('assignments/', include('tracker.urls')),
    path("", include("tracker.urls")),
   # path('accounts/', include('django.contrib.auth.urls')),  # login/logout
    
    
    path('accounts/login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG: ####### REMOVE DEPLOYING
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




