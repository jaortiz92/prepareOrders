from django.db import models
from django.db.models.base import Model
from idType import IdType


class Customer(models.Model):
    id = models.AutoField('ID', primary_key=True)
    id_siggo = models.CharField('ID Siigo', max_length=50)
    type_customer = models.CharField('Tipo Cliente', max_length=50)
    person_type = models.CharField('Tipo Persona', max_length=20)
    id_type = models.ForeignKey(IdType, on_delete=models.CASCADE)
    identification = models.CharField('Identificación', max_length=30)
    branch_office = models.IntegerField('Oficina')
    check_digit = models.IntegerField('Identificación')
    name = models