from django.shortcuts import render

# Create your views here.


from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from .models import Blog
from .serializers import BlogSerializer


@api_view(['GET','POST'])
def blog_list(request, *args, **kwargs):
    # get all the blog ,serialize them ,return them
    
    if request.method== 'GET':
        queryset=Blog.objects.all()
        serializer=BlogSerializer(queryset, many=True)
        return JsonResponse({'Blog':serializer.data})     #  OR   return JsonResponse(serializer.data,safe=False)
    
    if request.method == 'POST':
        serializer=BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
