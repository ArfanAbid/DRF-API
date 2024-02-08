from rest_framework import serializers
from .models import Blog

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