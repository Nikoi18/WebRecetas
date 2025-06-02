from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = Category
        fields = '__all__'
        #fields =('name','slug')
       # fields = ('__all__')
