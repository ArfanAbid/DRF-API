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
        return Response({'Blog':serializer.data})     #  OR   return JsonResponse(serializer.data,safe=False)
    
    if request.method == 'POST':
        serializer=BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)



@api_view(['GET','PUT','DELETE'])
def blog_detail(request ,id):
    try:
        query=Blog.objects.get(pk=id)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    


    if request.method=='GET':
        serializer=BlogSerializer(query)
        return Response(data=serializer.data)
    
    if request.method=='PUT':
        serializer=BlogSerializer(query,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    if request.method=='DELETE':
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
