from django.db import models
from autoslug import AutoSlugField
from categories.models import Category

# Create your models here.




class Recipe(models.Model):
    category = models.ForeignKey(Category, models.DO_NOTHING, verbose_name='Categoría', null= False)
    name = models.CharField(max_length=200, verbose_name='Nombre', null= False)
    slug = AutoSlugField(populate_from='name', max_length=100) # type: ignore
    time = models.CharField(max_length=100, verbose_name='Tiempo', null= False)
    photo = models.CharField(max_length=100, verbose_name='Foto', null= False)
    description = models.TextField(verbose_name='Descripción', null= False)
    date = models.DateTimeField(verbose_name='Fecha', auto_now_add=True)    


    def __str__(self):
        return self.name
    

    class Meta:
        db_table = 'recipes'
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'

