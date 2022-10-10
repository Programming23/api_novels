from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.views.static import serve


urlpatterns = [
    path('novels/', views.get_novels, name='novels'),
    path('novel/<int:pk>/', views.get_novel, name='novel'),
    path('chapter/<int:pk>/',
         views.get_content, name='get_content'),
    path('get_last_chapters/',
         views.get_last_chapters, name='get_last_chapters'),
    path('add_chapters/',
         views.add_chapters, name='add_chapters'),

]
