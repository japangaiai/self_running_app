from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LogoutView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('result/', views.result, name='result')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
