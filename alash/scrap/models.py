from django.db import models


class TempTable(models.Model):

    vend_code = models.CharField(max_length=50, verbose_name='Артикул')
    model = models.CharField(max_length=50)

    def __str__(self):
        return self.vend_code