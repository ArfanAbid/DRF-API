from django.shortcuts import render

# Create your views here.


from django.http import JsonResponse
from rest_framework.decorators import api_view


from .models import Blog
from .serializers import BlogSerializer


@api_view(['GET','POST'])
def blog_list(request, *args, **kwargs):
    # get all the blog ,serialize them ,return them
    queryset=Blog.objects.all()
    serializer=BlogSerializer(queryset, many=True)
    return JsonResponse({'Blog':serializer.data})     #  OR   return JsonResponse(serializer.data,safe=False)