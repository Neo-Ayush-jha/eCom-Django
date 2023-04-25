from django.contrib import admin
from django.urls import path
from shop.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",HomeView.as_view(),name="home"),
    path("singup/private/",PrivateView.as_view(),name="private_user_singup"),
    path("singup/public/",PublicView.as_view(),name="public_user_singup"),
    path("login/",LoginView.as_view(),name="login_user"),
    path("logout/user/",LogoutView.as_view(),name="logout"),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)