from django.shortcuts import render

# Create your views here.


from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics,mixins
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from .models import Blog
from .serializers import BlogSerializer,UserSerializers
from django.contrib.auth.models import User

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
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
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
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]    

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
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]     
    
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
        
    # This is additional method if u wants so :
    
    # def perform_create(self, serializer):
    #     title=self.get('title') or None
    #     if title is None:
    #         title="title is required or not Provided "
    #         serializer.save(title=title)    
    
        
class BlogRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated] 

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



    # Mixins with Generics 

# Mixins are used with generics in Django REST Framework to provide additional functionality and behavior to generic views. They allow developers to reuse common functionality across multiple views without duplicating code.

class ListCreate(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated] 

    queryset=Blog.objects.all()
    serializer_class=BlogSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    

class RetrieveUpdateDestroy(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated] 

    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    lookup_field='pk'

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)
    

# U can also use each functionality indenpendently using seperate function like mixins.UpdateModelMixins ... ect
    

# Token Authentication

class RegisterUser(APIView): # whenever user is created then token will be generated manually by this method
    def post(self, request):
        serializer=UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user=User.objects.get(username=serializer.data['username'])
            token_obj,_=Token.objects.get_or_create(user=user)

            Response_data={'data':serializer.data,'token':str(token_obj)}
            return Response(Response_data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)