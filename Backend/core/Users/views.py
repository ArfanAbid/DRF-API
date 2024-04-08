from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,logout



class UserRegister(APIView):
    """
    API endpoint that allows users to be registered.
    """

    def post(self, request ):
        try:
            serializer = RegisterSerializers(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Account created successfully'},status=status.HTTP_201_CREATED)
                # return JsonResponse({'message': 'Account created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class UserLogin(APIView):
    """
    API endpoint that allows users to login.
    """
    def post(self, request):
        try:

            serializer = LoginSerializer(data=request.data)
            # Check if the data is valid according to the serializer's validation rules
            if serializer.is_valid():
                # Extract username and password from validated data
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']

                user = authenticate(username=username, password=password)
                if user is not None:
                    # if you're implementing token-based authentication, you don't need to use login(request, user) because token-based authentication is stateless. Instead, you would typically generate a token upon successful authentication and return it to the client.   
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'message': 'Successfully logged in',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }, status=status.HTTP_200_OK)
                else:
                    # If authentication fails, return an error response
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    """
    API endpoint that allows users to logout.
    """
    def post(self, request):
        try:
            logout(request)
            return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)