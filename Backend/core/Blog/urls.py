from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list), # Function based
    path('<int:id>', views.blog_detail), # Function based
    path('list/', views.ListBlog.as_view()), # Class based
    path('detail/<int:pk>/', views.DetailBlog.as_view()), # Class based
    
]