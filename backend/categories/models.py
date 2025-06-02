from autoslug import AutoSlugField
from django.db import models


class Category(models.Model):

    
    name = models.CharField(max_length=20, verbose_name='Nombre', null= False)
    slug = AutoSlugField(populate_from='name')


    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']



