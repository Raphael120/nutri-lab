from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Ativacao(models.Model):
    token = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = ('Ativação')
        verbose_name_plural = ('Ativações')
