from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list),
    path('<int:id>', views.blog_detail),
    
]