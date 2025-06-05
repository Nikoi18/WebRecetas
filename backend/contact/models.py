from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre', null= False)
    email = models.EmailField(max_length=30, verbose_name='Correo', null= False)
    phone = models.IntegerField(verbose_name='Teléfono', null= False)
    message = models.TextField(verbose_name='Mensaje', null= False)
    date = models.DateTimeField(verbose_name='Fecha', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'contact'
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'