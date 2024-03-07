from django.urls import path
from Chat import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.login_view,name="login" ),
    path('register/',views.register,name="register" ),
    path('logout/',views.logout_view,name="logout" ),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
