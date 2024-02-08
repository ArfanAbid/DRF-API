from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list), # Function based
    path('<int:id>', views.blog_detail), # Function based
    path('list/', views.ListBlog.as_view()), # Class based
    path('detail/<int:pk>/', views.DetailBlog.as_view()), # Class based
    path('listcreate/', views.BlogListCreatAPI.as_view()), # Generics Class based
    path('updateDel/<int:pk>/', views.BlogRetrieveUpdateDestroyAPIView.as_view()), #  Generics Class based
    
]