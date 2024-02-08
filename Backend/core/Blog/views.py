from django.shortcuts import render

# Create your views here.


from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics


from .models import Blog
from .serializers import BlogSerializer

# There are many ways to write views in DRF which are listed below :

    # Function based views

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


    # Class based Views


class ListBlog(APIView):
    
    def get(self,request,*args,**kwargs):
        queryset=Blog.objects.all()
        serializer=BlogSerializer(queryset,many=True)
        return Response({'Blog':serializer.data})
    
    def post(self,request,*args,**kwargs):
        serializer=BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Blog':serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DetailBlog(APIView):

    def get(self, request,pk,*args, **kwargs):
        try:
            query=Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer=BlogSerializer(query)
        return Response(serializer.data)

    def put(self,request,pk,*args, **kwargs):
        try:
            query=Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer=BlogSerializer(query,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,*args, **kwargs):
        try:
            query=Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)     

        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)       
    

    # Generics Views

class BlogListCreatAPI(generics.ListCreateAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
        
    # This is additional method if u wants so :
    
    # def perform_create(self, serializer):
    #     title=self.get('title') or None
    #     if title is None:
    #         title="title is required or not Provided "
    #         serializer.save(title=title)    
    
        
class BlogRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    lookup_field='pk'

    # This is additional method if u wants so  You can add custom queryset logic here if needed.

    def perform_destroy(self, instance):
    # Your custom logic for deleting the blog entry
        instance=self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
            
'''            There are many other methods in generics u can use according to your use :
            CreateAPIView DestroyAPIView RetrieveDestroyAPIView ListAPIView ...  ect'''


