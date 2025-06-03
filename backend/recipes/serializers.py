from rest_framework import serializers
from .models import Recipe
from django.conf import settings



class RecipeSerializer(serializers.ModelSerializer):
    #categorie = serializers.ReadOnlyField(source='category.name')
    categorie = serializers.CharField(source='category.name')
    date = serializers.DateTimeField(format='%d-%m-%Y', read_only=True)
    image = serializers.SerializerMethodField()


    class Meta:
        model = Recipe
        #fields = '__all__'
        fields = ("id", "name", "slug", "time", "photo", "description", "date", "categorie", "image")

    def get_image(self, obj):
        return f"{settings.MEDIA_URL}upload/recipes/{obj.photo}"
        