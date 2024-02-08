from rest_framework import serializers
from .models import Blog
from django.contrib.auth.models import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','password')

        def create(self,attrs): # for hashing passwords
            user=User.objects.create(username=attrs['username'])
            user.set_password(attrs['password'])
            user.save()
            return user


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields=('id','title','content')
        
        #fields=__all__
        #exclude=('id)

        def validate_data(self, attrs):
            title =attrs.get('title')
            if Blog.objects.filter(title=title).exists(): 
                raise serializers.ValidationError("A blog with this title already exists.")
            return attrs