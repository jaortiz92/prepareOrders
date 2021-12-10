from django.db import models

class IdType(models.Model):
    code = models.CharField('Codigo',  max_length=2)
    name = models.CharField('Nombre del cogigo', max_length=50)
    