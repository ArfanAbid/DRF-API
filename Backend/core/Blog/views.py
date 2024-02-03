from django.shortcuts import render

# Create your views here.


from django.http import JsonResponse


from .models import Blog
from .serializers import BlogSerializer



def blog_list(request, *args, **kwargs):
    # get all the blog ,serialize them ,return them
    queryset=Blog.objects.all()
    serializer=BlogSerializer(queryset, many=True)
    return JsonResponse({'Blog':serializer.data},safe=False)     #  OR   return JsonResponse(serializer.data,safe=False)