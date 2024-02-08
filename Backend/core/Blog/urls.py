from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list), # Function based
    path('<int:id>', views.blog_detail), # Function based
    path('list/', views.ListBlog.as_view()), # Class based
    path('detail/<int:pk>/', views.DetailBlog.as_view()), # Class based
    path('listCreate/', views.BlogListCreatAPI.as_view()), # Generics Class based
    path('updateDel/<int:pk>/', views.BlogRetrieveUpdateDestroyAPIView.as_view()), #  Generics Class based
    path('createList/', views.ListCreate.as_view()), #  Mixins-Generics Class based
    path('reteriveUpdateDestroy/<int:pk>/', views.RetrieveUpdateDestroy.as_view()), #  Mixins-Generics Class based
    
]