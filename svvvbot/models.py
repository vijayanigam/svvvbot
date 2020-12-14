from django.db import models

# Create your models here.
class msgs(models.Model):
    id=models.IntegerField(primary_key=True)
    message = models.CharField(max_length=500)

    def __str__(self):
        return self.message



class reply(models.Model):
    id = models.IntegerField(primary_key=True)
    reply = models.CharField(max_length=500)

    def __str__(self):
        return self.reply
